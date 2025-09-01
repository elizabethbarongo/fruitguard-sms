#!/usr/bin/env python3
"""
Test different SMS endpoint variations to find the correct one
"""

import requests
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

def test_sms_endpoints():
    """Test different SMS endpoint variations"""
    
    api_key = os.getenv('API_key')
    api_secret = os.getenv('API_secret')
    
    if not api_key or not api_secret:
        print("❌ Missing API credentials")
        return
    
    # Create Basic Auth headers
    credentials = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}'
    }
    
    base_url = "https://api.smsleopard.com/v1"
    
    # Test different SMS endpoint variations
    sms_endpoints = [
        "/sms/send",
        "/sms",
        "/send",
        "/message/send",
        "/message",
        "/text/send",
        "/text"
    ]
    
    # Test payload
    payload = {
        'source': 'FruitGuard',
        'message': 'Test message',
        'destination': [{'number': '+254742252910'}]
    }
    
    print("=== Testing SMS Endpoint Variations ===")
    print(f"Base URL: {base_url}")
    print(f"Headers: {headers}")
    print()
    
    for endpoint in sms_endpoints:
        url = f"{base_url}{endpoint}"
        print(f"Testing: {endpoint}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}...")
            
            if response.status_code in [200, 201]:
                print(f"  ✅ SUCCESS! Found working SMS endpoint: {url}")
                return url
            elif response.status_code == 401:
                print(f"  ❌ Unauthorized - authentication issue")
            elif response.status_code == 404:
                print(f"  ❌ Not Found - endpoint doesn't exist")
            elif response.status_code == 400:
                print(f"  ⚠️  Bad Request - endpoint exists but payload issue")
            else:
                print(f"  ❓ Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}...")
        
        print()
    
    print("❌ No working SMS endpoints found")
    return None

def test_sender_id_alternatives():
    """Test different sender ID alternatives"""
    
    api_key = os.getenv('API_key')
    api_secret = os.getenv('API_secret')
    
    if not api_key or not api_secret:
        print("❌ Missing API credentials")
        return
    
    # Create Basic Auth headers
    credentials = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}'
    }
    
    # Test with working endpoint (if we found one) or common endpoint
    base_url = "https://api.smsleopard.com/v1"
    endpoint = "/sms/send"  # We'll test this with different sender IDs
    
    # Test different sender ID formats
    sender_ids = [
        "FruitGuard",
        "FRUITGUARD", 
        "fruitguard",
        "Fruit",
        "Guard",
        "Test",
        "TEST",
        "SMS",
        "Info",
        "Alert"
    ]
    
    print("=== Testing Different Sender IDs ===")
    
    for sender_id in sender_ids:
        payload = {
            'source': sender_id,
            'message': f'Test message from {sender_id}',
            'destination': [{'number': '+254742252910'}]
        }
        
        url = f"{base_url}{endpoint}"
        print(f"Testing sender ID: {sender_id}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}...")
            
            if response.status_code in [200, 201]:
                print(f"  ✅ SUCCESS! Working sender ID: {sender_id}")
                return sender_id
            elif "Unrecognized sender id" in response.text:
                print(f"  ❌ Sender ID '{sender_id}' not recognized")
            elif "not assigned to the account" in response.text:
                print(f"  ❌ Sender ID '{sender_id}' not assigned to account")
            else:
                print(f"  ❓ Other issue: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}...")
        
        print()
    
    print("❌ No working sender IDs found")
    return None

if __name__ == "__main__":
    print("🔍 Testing SMSLeopard API endpoints and sender IDs...")
    print()
    
    # Test endpoints first
    working_endpoint = test_sms_endpoints()
    
    if working_endpoint:
        print(f"\n🎉 Found working SMS endpoint: {working_endpoint}")
    else:
        print("\n❌ No working SMS endpoints found")
    
    print()
    
    # Test sender IDs
    working_sender_id = test_sender_id_alternatives()
    
    if working_sender_id:
        print(f"\n🎉 Found working sender ID: {working_sender_id}")
    else:
        print("\n❌ No working sender IDs found")
    
    print("\n💡 Recommendations:")
    print("1. Check SMSLeopard dashboard for approved sender IDs")
    print("2. Verify API documentation for correct endpoints")
    print("3. Contact SMSLeopard support if issues persist")
