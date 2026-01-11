from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Admin(UserMixin, db.Model):
    """Admin user for the system"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Person(db.Model): 
    """Registered person for face recognition"""
    __tablename__ = 'persons'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    student_id = db.Column(db.String(50), unique=True)  # Student ID
    photo_path = db.Column(db.String(255))  # Path to reference photo
    face_encoding = db.Column(db.LargeBinary)  # Stored face encoding
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    attendance_records = db.relationship('Attendance', backref='person', lazy='dynamic')
    
    def __repr__(self):
        return f'<Person {self.name}>'


class Attendance(db.Model):
    """Attendance record"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date = db.Column(db.Date, default=lambda: datetime.now().date(), nullable=False)
    status = db.Column(db.String(20), default='present')  # present, late, absent
    confidence = db.Column(db.Float)  # Face recognition confidence score
    
    def __repr__(self):
        return f'<Attendance {self.person.name} - {self.timestamp}>'
