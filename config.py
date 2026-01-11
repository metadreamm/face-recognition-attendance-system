import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration (SQLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database', 'attendance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Face recognition settings
    KNOWN_FACES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'known_faces')
    FACE_RECOGNITION_TOLERANCE = 0.6
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
