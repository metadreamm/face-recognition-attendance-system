import os
import base64
import pickle
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, jsonify, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date
from io import StringIO
import csv
import face_recognition
from app import db
from app.models import Admin, Person, Attendance

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Home page with live camera feed"""
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            return redirect(url_for('main.dashboard'))
        flash('Nieprawidłowa nazwa użytkownika lub hasło', 'error')
    
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard with attendance overview"""
    today = date.today()
    today_attendance = Attendance.query.filter_by(date=today).all()
    total_persons = Person.query.count()
    present_today = len(today_attendance)
    
    return render_template('dashboard.html', 
                         today_attendance=today_attendance,
                         total_persons=total_persons,
                         present_today=present_today)


@main.route('/persons')
@login_required
def persons():
    """List all registered persons"""
    all_persons = Person.query.all()
    return render_template('persons.html', persons=all_persons)


@main.route('/persons/add', methods=['GET', 'POST'])
@login_required
def add_person():
    """Add new person with reference photo"""
    if request.method == 'POST':
        # Collect form data once
        form_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'student_id': request.form.get('student_id')
        }

        name = form_data['name']
        email = form_data['email']
        student_id = form_data['student_id']
        camera_photo = request.form.get('camera_photo')  # Base64 from webcam
        file_photo = request.files.get('photo')  # Uploaded file
        
        if not name:
            flash('Imię jest wymagane', 'error')
            return render_template('add_person.html', **form_data)
        
        if student_id:
            existing = Person.query.filter_by(student_id=student_id).first()
            if existing:
                flash('Osoba z takim ID studenta już istnieje', 'error')
                return render_template('add_person.html', **form_data)
            
        if email:
            existing = Person.query.filter_by(email=email).first()
            if existing:
                flash('Osoba z takim adresem email już istnieje', 'error')
                return render_template('add_person.html', **form_data)
        
        # Process photo
        photo_path = None
        face_encoding = None
        
        try:
            if camera_photo:
                # Decode base64 webcam photo
                header, data = camera_photo.split(',', 1)
                image_data = base64.b64decode(data)
                filename = secure_filename(f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
                photo_path = os.path.join(current_app.config['KNOWN_FACES_DIR'], filename)
                with open(photo_path, 'wb') as f:
                    f.write(image_data)
            elif file_photo and file_photo.filename:
                # Save uploaded file
                filename = secure_filename(f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_photo.filename}")
                photo_path = os.path.join(current_app.config['KNOWN_FACES_DIR'], filename)
                file_photo.save(photo_path)
            
            if photo_path:
                # Generate face encoding
                image = face_recognition.load_image_file(photo_path)
                
                # Quick face detection first (faster with 'hog' model)
                face_locations = face_recognition.face_locations(image, model='hog')

                if not face_locations:
                    flash('Nie wykryto twarzy na zdjęciu. Spróbuj ponownie.', 'error')
                    os.remove(photo_path)
                    return render_template('add_person.html', **form_data)
                
                if len(face_locations) > 1:
                    flash('Wykryto więcej niż jedną twarz. Prześlij zdjęcie z jedną osobą.', 'error')
                    os.remove(photo_path)
                    return render_template('add_person.html', **form_data)
                
                # Generate encoding only after face is found
                encodings = face_recognition.face_encodings(image, face_locations)
                face_encoding = pickle.dumps(encodings[0])
            else:
                flash('Zdjęcie jest wymagane do rozpoznawania twarzy', 'error')
                return render_template('add_person.html', **form_data)
                
        except Exception as e:
            flash(f'Błąd przetwarzania zdjęcia: {str(e)}', 'error')
            return render_template('add_person.html', **form_data)
        
        person = Person(
            name=name, 
            email=email, 
            student_id=student_id,
            photo_path=filename if photo_path else None,
            face_encoding=face_encoding
        )
        db.session.add(person)
        db.session.commit()
        
        flash(f'Osoba {name} została dodana', 'success')
        return redirect(url_for('main.persons'))
    
    return render_template('add_person.html')


@main.route('/persons/delete/<int:id>')
@login_required
def delete_person(id):
    """Delete a person"""
    person = Person.query.get_or_404(id)

    # Delete attendance records first
    Attendance.query.filter_by(person_id=id).delete()

    # Delete photo file if exists
    if person.photo_path:
        photo_full_path = os.path.join(current_app.config['KNOWN_FACES_DIR'], person.photo_path)
        if os.path.exists(photo_full_path):
            os.remove(photo_full_path)

    db.session.delete(person)
    db.session.commit()
    flash(f'Osoba {person.name} została usunięta', 'success')
    return redirect(url_for('main.persons'))


@main.route('/persons/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_person(id):
    person = Person.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email')
        student_id = request.form.get('student_id')

        # Validation - check for duplicates
        if student_id:
            existing = Person.query.filter_by(student_id=student_id).first()
            if existing and existing.id != person.id:
                flash('Osoba z takim ID studenta już istnieje', 'error')
                return render_template('edit_person.html', person=person)
            
        if email:
            existing = Person.query.filter_by(email=email).first()
            if existing and existing.id != person.id:
                flash('Osoba z takim adresem email już istnieje', 'error')
                return render_template('edit_person.html', person=person)
        
        # Update only after validation passes
        person.name = name
        person.email = email
        person.student_id = student_id
        db.session.commit()
        flash('Dane osoby zostały zaktualizowane!', 'success')
        return redirect(url_for('main.persons'))
    
    return render_template('edit_person.html', person=person)


@main.route('/known_faces/<filename>')
@login_required
def known_faces(filename):
    return send_from_directory(current_app.config['KNOWN_FACES_DIR'], filename)


@main.route('/attendance')
@login_required
def attendance():
    """View attendance records"""
    selected_date = request.args.get('date', date.today().isoformat())
    records = Attendance.query.filter_by(date=selected_date).all()
    return render_template('attendance.html', records=records, selected_date=selected_date)


@main.route('/reports')
@login_required
def reports():
    """Generate attendance reports"""
    persons = Person.query.all()
    return render_template('reports.html', persons=persons)


@main.route('/reports/daily')
@login_required
def daily_report():
    date_str = request.args.get('date')
    if not date_str:
        flash('Wybierz datę', 'error')
        return redirect(url_for('main.reports'))
    
    report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    records = Attendance.query.filter_by(date=report_date).all()

    # Generate CSV
    output = StringIO()
    output.write('\ufeff') # BOM (Byte Order Mark) - ensures proper UTF-8 encoding detection (e.g., for Polish characters) 
    writer = csv.writer(output)
    writer.writerow(['Imię i nazwisko', 'ID studenta', 'Godzina', 'Status'])
    for r in records:
             writer.writerow([r.person.name, r.person.student_id or '-',
                             r.timestamp.strftime('%H:%M:%S'), r.status])
             
    output.seek(0)
    return Response(output.getvalue(), mimetype='text/csv; charset=utf-8',
                    headers={'Content-Disposition': f'attachment;filename=raport_{date_str}.csv'})


@main.route('/reports/monthly')
@login_required
def monthly_report():
    month_str = request.args.get('month') # format 2026-01
    if not month_str:
        flash('Wybierz miesiąc', 'error')
        return redirect(url_for('main.reports'))
    
    year, month = map(int, month_str.split('-'))
    from calendar import monthrange
    start_date = date(year, month, 1)
    end_date = date(year, month, monthrange(year, month)[1])

    records = Attendance.query.filter(
        Attendance.date >= start_date,
        Attendance.date <= end_date
    ).order_by(Attendance.date).all()

    output = StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    writer.writerow(['Data', 'Imię i nazwisko', 'ID studenta', 'Godzina', 'Status'])
    for r in records:
        writer.writerow([r.date.strftime('%Y-%m-%d'), r.person.name,
                        r.person.student_id or '-', r.timestamp.strftime('%H:%M:%S'), r.status])

    output.seek(0)
    return Response(output.getvalue(), mimetype='text/csv; charset=utf-8',
                    headers={'Content-Disposition': f'attachment;filename=raport_{month_str}.csv'})


@main.route('/reports/person')
@login_required
def person_report():
    person_id = request.args.get('person_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    if not person_id:
        flash('Wybierz osobę', 'error')
        return redirect(url_for('main.reports'))
    
    # Validate date range
    if date_from and date_to and date_from > date_to:
        flash('Data "Od" nie może być późniejsza niż data "Do"', 'error')
        return redirect(url_for("main.reports"))
    
    person = Person.query.get_or_404(person_id)
    
    query = Attendance.query.filter_by(person_id=person_id)

    if date_from:
        query = query.filter(Attendance.date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    if date_to:
        query = query.filter(Attendance.date <= datetime.strptime(date_to, '%Y-%m-%d').date())

    records = query.order_by(Attendance.date).all()

    output = StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    writer.writerow(['Osoba', person.name])
    writer.writerow(['ID studenta', person.student_id or '-'])
    writer.writerow([])
    writer.writerow(['Data', 'Godzina', 'Status'])
    for r in records:
        writer.writerow([r.date.strftime('%Y-%m-%d'), r.timestamp.strftime('%H:%M:%S'), r.status])

    output.seek(0)
    filename = f"raport_{person.name.replace(' ', '_')}_{date_from or 'all'}_{date_to or 'all'}.csv"
    return Response(output.getvalue(), mimetype='text/csv; charset=utf-8',
                    headers={'Content-Disposition': f'attachment;filename={filename}'})


# Face recognition API
@main.route('/api/recognize', methods=['POST'])
def recognize_face():
    """Receive image from camera and try to recognize face"""
    data = request.get_json()
    image_data = data.get('image')
    
    if not image_data:
        return jsonify({'success': False, 'error': 'Brak obrazu'})
    
    try:
        # Decode base64 image
        header, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        
        # Save to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            f.write(image_bytes)
            temp_path = f.name
        
        # Load image and find faces
        image = face_recognition.load_image_file(temp_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        # Remove temp file
        os.unlink(temp_path)
        
        if not face_encodings:
            return jsonify({'success': True, 'faces': []})
        
        # Load known faces from database
        known_persons = Person.query.all()
        known_encodings = []
        known_ids = []
        known_names = []
        
        for p in known_persons:
            if p.face_encoding:
                known_encodings.append(pickle.loads(p.face_encoding))
                known_ids.append(p.id)
                known_names.append(p.name)
        
        results = []
        today = date.today()
        
        for i, face_encoding in enumerate(face_encodings):
            top, right, bottom, left = face_locations[i]
            
            name = "Nieznany"
            person_id = None
            confidence = 0
            
            if known_encodings:
                # Compare with known faces
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match = distances.argmin()
                
                if distances[best_match] < 0.6:  # match threshold
                    person_id = known_ids[best_match]
                    name = known_names[best_match]
                    confidence = round(1 - distances[best_match], 2)
                    
                    # Auto mark attendance
                    existing = Attendance.query.filter_by(person_id=person_id, date=today).first()
                    if not existing:
                        attendance = Attendance(
                            person_id=person_id,
                            date=today,
                            confidence=confidence
                        )
                        db.session.add(attendance)
                        db.session.commit()
            
            results.append({
                'name': name,
                'person_id': person_id,
                'confidence': confidence,
                'box': {'top': top, 'right': right, 'bottom': bottom, 'left': left}
            })
        
        return jsonify({'success': True, 'faces': results})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@main.route('/api/mark_attendance', methods=['POST'])
def mark_attendance():
    """API endpoint to mark attendance after face recognition"""
    data = request.get_json()
    person_id = data.get('person_id')
    confidence = data.get('confidence')
    
    if not person_id:
        return jsonify({'error': 'Person ID required'}), 400
    
    person = Person.query.get(person_id)
    if not person:
        return jsonify({'error': 'Person not found'}), 404
    
    # Check if already marked today
    today = date.today()
    existing = Attendance.query.filter_by(person_id=person_id, date=today).first()
    if existing:
        return jsonify({'message': 'Already marked', 'person': person.name}), 200
    
    attendance = Attendance(
        person_id=person_id,
        date=today,
        confidence=confidence
    )
    db.session.add(attendance)
    db.session.commit()
    
    return jsonify({'message': 'Attendance marked', 'person': person.name}), 201
