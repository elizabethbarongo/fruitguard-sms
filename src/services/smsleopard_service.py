import requests
import time
import re
import base64
from typing import Dict, List, Optional, Tuple
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SMSLeopardService:
    """Service class for interacting with SMSLeopard API"""
    
    def __init__(self):
        self.api_key = Config.SMSLEOPARD_API_KEY
        self.api_secret = Config.SMSLEOPARD_API_SECRET
        self.api_url = Config.SMSLEOPARD_API_URL
        
        # Create base64 encoded credentials for Basic auth
        if self.api_key and self.api_secret:
            credentials = f"{self.api_key}:{self.api_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            self.headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
        else:
            self.headers = {'Content-Type': 'application/json'}
            logger.warning("SMSLeopard API key or secret not configured")
    
    def send_sms(self, 
                 phone_numbers: List[str], 
                 message: str, 
                 sender_id: Optional[str] = None,
                 schedule_time: Optional[str] = None) -> Dict:
        """
        Send SMS message(s) using SMSLeopard API
        
        Args:
            phone_numbers: List of phone numbers to send SMS to
            message: The message content
            sender_id: Custom sender ID (optional)
            schedule_time: Schedule time in ISO format (optional)
            
        Returns:
            API response dictionary
        """
        if not self.api_key or not self.api_secret:
            raise ValueError("SMSLeopard API key or secret not configured")
        
        if not phone_numbers:
            raise ValueError("Phone numbers list cannot be empty")
        
        if not message:
            raise ValueError("Message cannot be empty")
        
        # SMSLeopard API payload format
        destinations = [{"number": number} for number in phone_numbers]
        payload = {
            'source': sender_id or Config.DEFAULT_SENDER_ID,
            'message': message,
            'destination': destinations
        }
        if schedule_time:
            payload['schedule_time'] = schedule_time
        logger.info(f"Sending SMS to {len(phone_numbers)} recipients")
        try:
            response = requests.post(
                f"{self.api_url}/sms/send",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"SMS sent successfully. Message ID: {result.get('message_id')}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            raise
    
    def send_sms_with_retry(self, 
                           phone_numbers: List[str], 
                           message: str, 
                           sender_id: Optional[str] = None,
                           max_retries: Optional[int] = None) -> Dict:
        """
        Send SMS with retry mechanism
        
        Args:
            phone_numbers: List of phone numbers to send SMS to
            message: The message content
            sender_id: Custom sender ID (optional)
            max_retries: Maximum number of retries (optional)
            
        Returns:
            API response dictionary
        """
        max_retries = max_retries or Config.MAX_RETRIES
        for attempt in range(max_retries + 1):
            try:
                return self.send_sms(phone_numbers, message, sender_id)
            except Exception as e:
                if attempt == max_retries:
                    logger.error(f"Failed to send SMS after {max_retries} retries")
                    raise
                logger.warning(f"SMS send attempt {attempt + 1} failed, retrying in {Config.RETRY_DELAY}s")
                time.sleep(Config.RETRY_DELAY)
    
    def get_sms_status(self, message_id: str) -> Dict:
        """
        Get SMS delivery status
        
        Args:
            message_id: The message ID to check
            
        Returns:
            Status information dictionary
        """
        if not self.api_key or not self.api_secret:
            raise ValueError("SMSLeopard API key or secret not configured")
        try:
            response = requests.get(
                f"{self.api_url}/sms/status/{message_id}",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get SMS status: {str(e)}")
            raise
    
    def get_balance(self) -> Dict:
        """
        Get account balance
        
        Returns:
            Balance information dictionary
        """
        if not self.api_key or not self.api_secret:
            raise ValueError("SMSLeopard API key or secret not configured")
        try:
            response = requests.get(
                f"{self.api_url}/account/balance",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get balance: {str(e)}")
            raise
    
    def validate_phone_number(self, phone_number: str) -> bool:
        """
        Validate phone number format
        
        Args:
            phone_number: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Basic validation - can be enhanced based on requirements
        pattern = r'^\+?[1-9]\d{9,14}$'
        return bool(re.match(pattern, phone_number))
    
    def format_phone_numbers(self, phone_numbers: List[str]) -> List[str]:
        """
        Format and validate phone numbers
        
        Args:
            phone_numbers: List of phone numbers to format
            
        Returns:
            List of formatted phone numbers
        """
        formatted_numbers = []
        invalid_numbers = []
        for number in phone_numbers:
            # Remove spaces and special characters
            cleaned = ''.join(filter(str.isdigit, number))
            # Add country code if not present (assuming +254 for Kenya)
            if cleaned.startswith('0') and len(cleaned) == 10:
                cleaned = '254' + cleaned[1:]
            elif len(cleaned) == 9:
                cleaned = '254' + cleaned
            elif cleaned.startswith('254') and len(cleaned) == 12:
                pass  # already correct
            elif cleaned.startswith('7') and len(cleaned) == 9:
                cleaned = '254' + cleaned
            elif cleaned.startswith('1') and len(cleaned) == 9:
                cleaned = '254' + cleaned
            elif cleaned.startswith('254') and len(cleaned) == 13:
                cleaned = cleaned[1:]  # remove leading 2 if double country code
            if self.validate_phone_number('+' + cleaned):
                formatted_numbers.append('+' + cleaned)
            else:
                invalid_numbers.append(number)
        if invalid_numbers:
            logger.warning(f"Invalid phone numbers: {invalid_numbers}")
        return formatted_numbers
