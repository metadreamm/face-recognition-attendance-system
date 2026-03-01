# Face Recognition Attendance System

A system for automatic attendance logging using facial recognition.

## Requirements

- Python 3.10 or 3.11 (recommended) – **Python 3.12+ may cause compatibility issues**
- Webcam
- Browser with JavaScript support
- Windows system (tested), Linux/macOS (not tested)

## Installation (Windows)

### Step 1: Install Python

1. Download [Python 3.10 or 3.11](https://www.python.org/downloads/)
2. During installation, check **"Add Python to PATH"**

> ⚠️ **Note:** Python 3.13 may cause compatibility issues with some libraries.

### Step 2: Install Visual Studio Build Tools

Required for compiling the `dlib` library (used by `face_recognition`).

1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Run the installer
3. Select **"Desktop development with C++"**
4. In the "Installation details" panel (on the right), select only:
   - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
   - ✅ Windows 10/11 SDK
5. Install and **restart your computer**

### Step 3: Install CMake (optional)

CMake is required to compile `dlib`. It usually installs automatically via `requirements.txt`, but if any errors occur:

1. Download [CMake](https://cmake.org/download/)
2. During installation, check **"Add CMake to PATH"**

Or install via pip (after creating the virtual environment):

```bash
pip install cmake
```

### Step 4: Clone the repository

```bash
git clone https://github.com/metadreamm/face-recognition-attendance-system
cd face-recognition-attendance-system
```

### Step 5: Create a virtual environment

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

Once activated, you'll see `(venv)` at the beginning of your command line.

### Step 6: Install dependencies

```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

> ⏱️ Installation may take 5–15 minutes (due to `dlib` compilation).

#### If errors occur with `requirements.txt`:

Try installing dependencies without strict version pins:

```bash
pip install Flask Flask-SQLAlchemy Flask-Login SQLAlchemy Werkzeug setuptools opencv-python face-recognition numpy Pillow python-dotenv
```

### Step 7: Run the application

```bash
python run.py
```

### Step 8: Open in your browser

```
http://127.0.0.1:5000
```

**Login credentials:** `admin` / `admin123`

---

## Troubleshooting

### "Microsoft Visual C++ 14.0 or greater is required"

→ Install Visual Studio Build Tools (Step 2)

### "CMake must be installed"

→ Run: `pip install cmake`

### "No module named 'face_recognition'"

→ Run: `pip install face_recognition --no-cache-dir`

### "No module named 'dotenv'"

→ Run: `pip install python-dotenv`

### SQLAlchemy errors on Python 3.13

→ Run: `pip install SQLAlchemy>=2.0.30 --upgrade`

### Warning "pkg_resources is deprecated"

→ Safe to ignore – it doesn't affect application functionality.

---

## Installation (Linux – not tested)

```bash
sudo apt update
sudo apt install python3-venv python3-dev cmake build-essential
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

---

## Installation (macOS – not tested)

```bash
brew install cmake python@3.11
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

---

## Features

- ✅ Register people using reference photos (via camera or upload)
- ✅ Real-time facial recognition using webcam
- ✅ Automatic attendance logging
- ✅ Prevent duplicate check-ins on the same day
- ✅ Attendance history with date filtering
- ✅ Reports: daily, monthly, individual (CSV export)
- ✅ Admin dashboard with login protection

---

## Project structure

```
├── app/                 # Application logic
│   ├── __init__.py      # Flask app factory
│   ├── models.py        # Database models
│   └── routes.py        # API endpoints and views
├── templates/           # HTML templates (Jinja2)
├── static/              # Static files (CSS)
├── known_faces/         # Reference face images
├── database/            # SQLite database
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
└── run.py               # Application entry point
```

---

## Technologies

- **Flask** – Python web framework
- **SQLAlchemy + SQLite** – database
- **face_recognition + dlib** – facial recognition (HOG algorithm)
- **Bootstrap 5** – user interface framework
- **JavaScript** – camera capture support (MediaDevices API)
