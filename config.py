import os
from datetime import timedelta

# Flask Configuration
class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-this')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    # Path Configuration
    LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

    # CORS Configuration
    CORS_ORIGINS = ['*']  # In production, specify allowed domains

    # Authentication
    DEFAULT_PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'admin123')  # Change this!

# Service Configuration - Add your custom services here
SERVICES = {
    'sample_service': {
        'name': 'Sample Service',
        'description': 'Example service for demonstration',
        'command': 'python -u example_script.py',
        'auto_restart': True,
        'enabled': True,
    },
}

# Create necessary directories
os.makedirs(Config.LOG_DIR, exist_ok=True)
os.makedirs(Config.DATA_DIR, exist_ok=True)
