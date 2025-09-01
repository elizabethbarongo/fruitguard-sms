import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the SMS application"""
    
    # SMSLeopard API Configuration
    API_KEY = os.getenv('API_key', '')
    API_SECRET = os.getenv('API_secret', '')
    ACCESS_TOKEN = os.getenv('Access_token', '')
    ENVIRONMENT = os.getenv('Environment', 'sandbox')
    
    # Set API URL based on environment
    if ENVIRONMENT == 'sandbox':
        API_URL = 'https://api.smsleopard.com/v1'  # SMSLeopard doesn't have separate sandbox URL
    else:
        API_URL = 'https://api.smsleopard.com/v1'
    
    # Webhook Configuration
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')
    WEBHOOK_ENDPOINT = os.getenv('WEBHOOK_ENDPOINT', '/dr')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # SMS Configuration
    DEFAULT_SENDER_ID = os.getenv('DEFAULT_SENDER_ID', 'FruitGuard')
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))  # seconds
    
    # Phone number configuration for Kenya
    DEFAULT_COUNTRY_CODE = '+254'  # Kenya
    KENYA_PHONE_PATTERN = r'^(\+254|254|0)?([17]\d{8})$'

