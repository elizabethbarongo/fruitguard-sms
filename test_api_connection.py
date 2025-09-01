#!/usr/bin/env python3
"""
Test script to check Africa's Talking API connection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import ssl
from src.config import Config

def test_api_connection():
    """Test connection to Africa's Talking API"""
    
    print("Testing Africa's Talking API Connection")
    print("=" * 50)
    
    # Test URLs
    urls = [
        "https://api.sandbox.africastalking.com/version1",
        "https://api.africastalking.com/version1",
        "http://api.sandbox.africastalking.com/version1",  # Try HTTP
        "http://api.africastalking.com/version1"  # Try HTTP
    ]
    
    for url in urls:
        print(f"\nTesting URL: {url}")
        try:
            # Try with SSL verification
            response = requests.get(f"{url}/user", timeout=10, verify=True)
            print(f"✓ Success with SSL verification - Status: {response.status_code}")
            break
        except requests.exceptions.SSLError as e:
            print(f"✗ SSL Error with verification: {e}")
            try:
                # Try without SSL verification
                response = requests.get(f"{url}/user", timeout=10, verify=False)
                print(f"✓ Success without SSL verification - Status: {response.status_code}")
                break
            except Exception as e2:
                print(f"✗ Failed without SSL verification: {e2}")
        except Exception as e:
            print(f"✗ Connection failed: {e}")
    
    print("\n" + "=" * 50)

def test_ssl_configuration():
    """Test SSL configuration"""
    
    print("Testing SSL Configuration")
    print("=" * 50)
    
    try:
        # Test SSL context
        context = ssl.create_default_context()
        print(f"✓ SSL context created successfully")
        print(f"  - SSL version: {ssl.OPENSSL_VERSION}")
        print(f"  - Default verify mode: {context.verify_mode}")
        print(f"  - Check hostname: {context.check_hostname}")
    except Exception as e:
        print(f"✗ SSL context creation failed: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_ssl_configuration()
    test_api_connection()
    
    print("Connection test completed!")

