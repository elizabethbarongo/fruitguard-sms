#!/usr/bin/env python3
"""Test common default sender IDs that SMSLeopard might provide"""

import requests
import os
from dotenv import load_dotenv
import base64

load_dotenv()

def test_default_senders():
    api_key = os.getenv('API_key')
    api_secret = os.getenv('API_secret')
    
    if not api_key or not api_secret:
        print("❌ Missing API credentials")
        return
    
    credentials = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}'
    }
    
    # Common default sender IDs that SMS providers often use
    default_senders = [
        "SMS", "INFO", "ALERT", "NOTIFY", "SYSTEM", "ADMIN", "SUPPORT",
        "HELP", "SERVICE", "UPDATE", "NEWS", "REMINDER", "VERIFY",
        "CODE", "OTP", "PIN", "SECURITY", "ACCESS", "LOGIN", "ACCOUNT"
    ]
    
    print("=== Testing Common Default Sender IDs ===")
    
    for sender in default_senders:
        payload = {
            'source': sender,
            'message': f'Test message from {sender}',
            'destination': [{'number': '+254742252910'}]
        }
        
        try:
            response = requests.post(
                "https://api.smsleopard.com/v1/sms/send",
                headers=headers, 
                json=payload,
                timeout=10
            )
            
            print(f"{sender}: {response.status_code} - {response.text[:100]}...")
            
            if response.status_code in [200, 201]:
                print(f"  ✅ SUCCESS! Working sender ID: {sender}")
                return sender
                
        except Exception as e:
            print(f"{sender}: Error - {str(e)[:50]}...")
    
    print("\n❌ No default sender IDs worked")
    return None

if __name__ == "__main__":
    working_sender = test_default_senders()
    
    if working_sender:
        print(f"\n🎉 Use sender ID: {working_sender}")
    else:
        print("\n💡 You need to:")
        print("1. Log into SMSLeopard dashboard")
        print("2. Check 'Sender IDs' or 'Brand Names' section")
        print("3. Request approval for 'FruitGuard' or use an approved one")
        print("4. Add credits to your account")
