#!/usr/bin/env python3
"""
Example script demonstrating how to use the Africa's Talking SMS service
with Kenyan phone numbers
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.smsleopard_service import AfricasTalkingService
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def send_test_sms():
    """Send a test SMS to demonstrate the service"""
    
    # Initialize the service
    sms_service = AfricasTalkingService()
    
    # Test phone numbers (replace with actual numbers for testing)
    test_numbers = [
        "+254712345678",  # Valid Kenyan number with +254
        "254712345678",   # Valid Kenyan number with 254
        "0712345678",     # Valid Kenyan number with 0
        "712345678",      # Valid Kenyan number without prefix
    ]
    
    # Test message
    message = "Hello from FruitGuard SMS! This is a test message from Africa's Talking API."
    
    try:
        # Send SMS
        logger.info("Sending test SMS...")
        result = sms_service.send_sms(
            phone_numbers=test_numbers,
            message=message,
            sender_id="FruitGuard"
        )
        
        logger.info(f"SMS sent successfully!")
        logger.info(f"Response: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to send SMS: {str(e)}")
        return None

def check_balance():
    """Check account balance"""
    
    sms_service = AfricasTalkingService()
    
    try:
        balance = sms_service.get_balance()
        logger.info(f"Account balance: {balance}")
        return balance
        
    except Exception as e:
        logger.error(f"Failed to get balance: {str(e)}")
        return None

def validate_numbers():
    """Validate and format phone numbers"""
    
    sms_service = AfricasTalkingService()
    
    # Test various phone number formats
    test_numbers = [
        "+254712345678",
        "254712345678", 
        "0712345678",
        "712345678",
        "+254123456789",  # Invalid (starts with 1)
        "123456789",      # Invalid (starts with 1)
    ]
    
    logger.info("Validating phone numbers...")
    
    for number in test_numbers:
        is_valid = sms_service.validate_phone_number(number)
        logger.info(f"{number}: {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    # Format all numbers
    formatted = sms_service.format_phone_numbers(test_numbers)
    logger.info(f"Formatted numbers: {formatted}")

if __name__ == "__main__":
    print("FruitGuard SMS - Africa's Talking Example")
    print("=" * 50)
    
    # Validate phone numbers
    validate_numbers()
    
    print("\n" + "=" * 50)
    
    # Check balance (if API is configured)
    check_balance()
    
    print("\n" + "=" * 50)
    
    # Send test SMS (uncomment to test)
    # send_test_sms()
    
    print("Example completed!")
    print("\nNote: To send actual SMS, uncomment the send_test_sms() call")
    print("and replace test phone numbers with real Kenyan numbers.")

