#!/usr/bin/env python3
"""Quick SMS test - will work once you have an approved sender ID"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.smsleopard_service import SMSLeopardService

def quick_test():
    """Quick test of the SMS service"""
    
    print("=== Quick SMS Test ===")
    
    try:
        service = SMSLeopardService()
        print("✅ Service initialized")
        
        # Test balance
        balance = service.get_balance()
        print(f"✅ Account balance: {balance['balance']} {balance['currency']}")
        
        # Test SMS send - CHANGE THIS SENDER ID to one approved in your account
        approved_sender_id = "YOUR_APPROVED_SENDER_ID"  # ← CHANGE THIS!
        
        print(f"\n📱 Testing SMS with sender ID: {approved_sender_id}")
        print("💡 If this fails, replace 'YOUR_APPROVED_SENDER_ID' with an approved sender ID from your dashboard")
        
        result = service.send_sms(
            phone_numbers=['+254742252910'],
            message='Test: FruitGuard SMS service is working!',
            sender_id=approved_sender_id
        )
        
        print(f"✅ SMS sent successfully: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 To fix this:")
        print("1. Log into SMSLeopard dashboard")
        print("2. Find an approved sender ID")
        print("3. Replace 'YOUR_APPROVED_SENDER_ID' in this script")
        print("4. Run the test again")

if __name__ == "__main__":
    quick_test()
