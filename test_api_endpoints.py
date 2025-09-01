#!/usr/bin/env python3
"""
Comprehensive test script to find correct SMSLeopard API endpoints and authentication
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smsleopard_api():
    """Test various SMSLeopard API endpoints and authentication methods"""
    
    # Get credentials from environment
    api_key = os.getenv('API_key')
    api_secret = os.getenv('API_secret')
    access_token = os.getenv('Access_token')
    
    print("=== SMSLeopard API Comprehensive Test ===")
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: NOT SET")
    print(f"API Secret: {api_secret[:10]}..." if api_secret else "API Secret: NOT SET")
    print(f"Access Token: {access_token[:10]}..." if access_token else "Access Token: NOT SET")
    print()
    
    # Test different base URLs
    base_urls = [
        "https://api.smsleopard.com/v1",
        "https://api.smsleopard.com/v2", 
        "https://api.smsleopard.com",
        "https://smsleopard.com/api/v1",
        "https://smsleopard.com/api"
    ]
    
    # Test different authentication methods
    auth_methods = []
    
    if api_key:
        auth_methods.append(("API Key in Headers", {'X-API-Key': api_key}))
        auth_methods.append(("API Key in Authorization", {'Authorization': f'Bearer {api_key}'}))
    
    if api_key and api_secret:
        import base64
        credentials = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
        auth_methods.append(("Basic Auth", {'Authorization': f'Basic {credentials}'}))
    
    if access_token:
        auth_methods.append(("Access Token", {'Authorization': f'Bearer {access_token}'}))
    
    # Test different endpoints
    endpoints = [
        "/",
        "/sms/send",
        "/sms",
        "/account",
        "/account/balance",
        "/balance",
        "/status",
        "/health",
        "/ping"
    ]
    
    for base_url in base_urls:
        print(f"\n=== Testing Base URL: {base_url} ===")
        
        for auth_name, auth_headers in auth_methods:
            print(f"\n--- {auth_name} ---")
            
            for endpoint in endpoints:
                url = f"{base_url}{endpoint}"
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    **auth_headers
                }
                
                try:
                    if endpoint in ["/sms/send"]:
                        # Test POST for SMS send endpoint
                        payload = {
                            'source': 'FruitGuard',
                            'message': 'Test message',
                            'destination': [{'number': '+254742252910'}]
                        }
                        response = requests.post(url, headers=headers, json=payload, timeout=10)
                    else:
                        # Test GET for other endpoints
                        response = requests.get(url, headers=headers, timeout=10)
                    
                    print(f"  {endpoint}: {response.status_code} - {response.text[:100]}...")
                    
                    # If we get a successful response, note it
                    if response.status_code in [200, 201]:
                        print(f"    ✅ SUCCESS! Found working endpoint: {url}")
                        print(f"    ✅ Working authentication: {auth_name}")
                        return url, auth_name, auth_headers
                        
                except Exception as e:
                    print(f"  {endpoint}: Error - {str(e)[:50]}...")
    
    print("\n❌ No working endpoints found with current credentials")
    return None, None, None

def test_specific_endpoint(url, auth_headers):
    """Test a specific working endpoint with SMS functionality"""
    print(f"\n=== Testing SMS Functionality at {url} ===")
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        **auth_headers
    }
    
    # Test payload based on what we found working
    payload = {
        'source': 'FruitGuard',
        'message': 'Test: FruitGuard API connection successful!',
        'destination': [{'number': '+254742252910'}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ SMS test successful!")
        else:
            print("❌ SMS test failed")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    working_url, working_auth, working_headers = test_smsleopard_api()
    
    if working_url and working_auth:
        print(f"\n🎉 Found working configuration:")
        print(f"   URL: {working_url}")
        print(f"   Auth: {working_auth}")
        
        # Test the working endpoint
        test_specific_endpoint(working_url, working_headers)
    else:
        print("\n🔍 Recommendations:")
        print("1. Check your SMSLeopard account dashboard for correct API endpoints")
        print("2. Verify your API credentials are correct and active")
        print("3. Check if you need to activate your account or add credits")
        print("4. Contact SMSLeopard support for API documentation")
