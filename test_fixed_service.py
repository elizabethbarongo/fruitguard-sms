#!/usr/bin/env python3
"""
Test script to verify the fixed SMSLeopard service
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.smsleopard_service import SMSLeopardService
from config import Config

def test_fixed_service():
    """Test the fixed SMS service"""
    
    print("=== Testing Fixed SMSLeopard Service ===")
    
    # Check configuration
    print(f"API Key: {Config.API_KEY[:10]}..." if Config.API_KEY else "API Key: NOT SET")
    print(f"API Secret: {Config.API_SECRET[:10]}..." if Config.API_SECRET else "API Secret: NOT SET")
    print(f"Access Token: {Config.ACCESS_TOKEN[:10]}..." if Config.ACCESS_TOKEN else "Access Token: NOT SET")
    print()
    
    if not Config.API_KEY or not Config.API_SECRET:
        print("❌ Missing API credentials. Please check your .env file")
        return
    
    try:
        # Initialize service
        service = SMSLeopardService()
        print("✅ Service initialized successfully")
        print(f"Headers: {service.headers}")
        print()
        
        # Test balance endpoint
        print("=== Testing Balance Endpoint ===")
        try:
            balance = service.get_balance()
            print(f"✅ Balance check successful: {balance}")
        except Exception as e:
            print(f"❌ Balance check failed: {e}")
        print()
        
        # Test SMS send (this might fail due to sender ID issue)
        print("=== Testing SMS Send ===")
        try:
            result = service.send_sms(
                phone_numbers=['+254742252910'],
                message='Test: FruitGuard service is now working!',
                sender_id='FruitGuard'  # This might need to be changed
            )
            print(f"✅ SMS sent successfully: {result}")
        except Exception as e:
            print(f"❌ SMS send failed: {e}")
            print("\n💡 This might be due to:")
            print("   - Sender ID 'FruitGuard' not being approved")
            print("   - Need to use a different sender ID")
            print("   - Account needs activation or credits")
        print()
        
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")

if __name__ == "__main__":
    test_fixed_service()
