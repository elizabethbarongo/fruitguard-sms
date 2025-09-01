#!/usr/bin/env python3
"""
Test script to diagnose SMSLeopard API authentication issues
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_connection():
    """Test different authentication methods with SMSLeopard API"""
    
    # Get credentials from environment
    api_key = os.getenv('API_key')
    api_secret = os.getenv('API_secret')
    access_token = os.getenv('Access_token')
    
    print("=== SMSLeopard API Credential Test ===")
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: NOT SET")
    print(f"API Secret: {api_secret[:10]}..." if api_secret else "API Secret: NOT SET")
    print(f"Access Token: {access_token[:10]}..." if access_token else "Access Token: NOT SET")
    print()
    
    base_url = "https://api.smsleopard.com/v1"
    
    # Test 1: Bearer token authentication (current method)
    if access_token:
        print("=== Test 1: Bearer Token Authentication ===")
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        try:
            response = requests.get(f"{base_url}/account/balance", headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
        print()
    
    # Test 2: Basic authentication with API key and secret
    if api_key and api_secret:
        print("=== Test 2: Basic Authentication ===")
        import base64
        credentials = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}'
        }
        
        try:
            response = requests.get(f"{base_url}/account/balance", headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
        print()
    
    # Test 3: API key in headers
    if api_key:
        print("=== Test 3: API Key in Headers ===")
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }
        
        try:
            response = requests.get(f"{base_url}/account/balance", headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
        print()
    
    # Test 4: Check if API endpoint exists
    print("=== Test 4: API Endpoint Check ===")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Base URL Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    test_api_connection()
