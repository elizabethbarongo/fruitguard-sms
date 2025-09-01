#!/usr/bin/env python3
"""
Test script to verify Kenyan phone number validation and formatting
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.services.smsleopard_service import AfricasTalkingService
import re

def test_kenyan_phone_validation():
    """Test Kenyan phone number validation"""
    print("Testing Kenyan Phone Number Validation")
    print("=" * 50)
    
    # Test cases for Kenyan phone numbers
    test_numbers = [
        "+254712345678",  # Valid with +254
        "254712345678",   # Valid with 254
        "0712345678",     # Valid with 0
        "712345678",      # Valid without prefix
        "+254123456789",  # Invalid (starts with 1, should be 7)
        "123456789",      # Invalid (starts with 1)
        "071234567",      # Invalid (too short)
        "07123456789",    # Invalid (too long)
        "abc123def",      # Invalid (contains letters)
        "",               # Invalid (empty)
    ]
    
    service = AfricasTalkingService()
    
    for number in test_numbers:
        is_valid = service.validate_phone_number(number)
        print(f"{number:15} -> {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    print("\n" + "=" * 50)

def test_phone_number_formatting():
    """Test phone number formatting"""
    print("Testing Phone Number Formatting")
    print("=" * 50)
    
    test_numbers = [
        "+254712345678",
        "254712345678", 
        "0712345678",
        "712345678",
        "+254123456789",  # Invalid
        "123456789",      # Invalid
    ]
    
    service = AfricasTalkingService()
    
    formatted = service.format_phone_numbers(test_numbers)
    print(f"Original numbers: {test_numbers}")
    print(f"Formatted numbers: {formatted}")
    
    print("\n" + "=" * 50)

def test_config():
    """Test configuration loading"""
    print("Testing Configuration")
    print("=" * 50)
    
    print(f"API Key: {Config.API_KEY[:10]}..." if Config.API_KEY else "API Key: Not set")
    print(f"Environment: {Config.ENVIRONMENT}")
    print(f"API URL: {Config.API_URL}")
    print(f"Default Country Code: {Config.DEFAULT_COUNTRY_CODE}")
    print(f"Kenya Phone Pattern: {Config.KENYA_PHONE_PATTERN}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_config()
    test_kenyan_phone_validation()
    test_phone_number_formatting()
    
    print("All tests completed!")

