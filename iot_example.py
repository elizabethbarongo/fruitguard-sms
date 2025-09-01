#!/usr/bin/env python3
"""
IoT Integration Example for FruitGuard SMS Service
This example shows how to integrate the SMS service with IoT devices
"""

import requests
import json
import time
from datetime import datetime

class FruitGuardIoT:
    """IoT integration class for FruitGuard SMS alerts"""
    
    def __init__(self, sms_api_url="http://localhost:5000"):
        self.sms_api_url = sms_api_url
        self.alert_recipients = []
        self.alert_thresholds = {
            'temperature': {'min': 15, 'max': 35},
            'humidity': {'min': 30, 'max': 80},
            'motion_detected': False,
            'intrusion_detected': False
        }
    
    def add_alert_recipient(self, phone_number):
        """Add a phone number to receive alerts"""
        self.alert_recipients.append(phone_number)
    
    def set_alert_thresholds(self, **thresholds):
        """Set alert thresholds for different sensors"""
        self.alert_thresholds.update(thresholds)
    
    def send_alert(self, alert_type, message, priority="normal"):
        """Send SMS alert to all recipients"""
        if not self.alert_recipients:
            print("No alert recipients configured")
            return
        
        # Add priority prefix to message
        if priority == "high":
            message = f"🚨 URGENT: {message}"
        elif priority == "medium":
            message = f"⚠️ ALERT: {message}"
        else:
            message = f"ℹ️ INFO: {message}"
        
        try:
            response = requests.post(
                f"{self.sms_api_url}/sms/send",
                headers={'Content-Type': 'application/json'},
                json={
                    'phone_numbers': self.alert_recipients,
                    'message': message,
                    'sender_id': 'FruitGuard'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"Alert sent successfully: {alert_type}")
            else:
                print(f"Failed to send alert: {response.text}")
                
        except Exception as e:
            print(f"Error sending alert: {str(e)}")
    
    def process_sensor_data(self, sensor_data):
        """Process sensor data and send alerts if thresholds are exceeded"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Temperature monitoring
        if 'temperature' in sensor_data:
            temp = sensor_data['temperature']
            if temp < self.alert_thresholds['temperature']['min']:
                self.send_alert(
                    'temperature_low',
                    f"Temperature too low: {temp}°C at {timestamp}",
                    priority="medium"
                )
            elif temp > self.alert_thresholds['temperature']['max']:
                self.send_alert(
                    'temperature_high',
                    f"Temperature too high: {temp}°C at {timestamp}",
                    priority="high"
                )
        
        # Humidity monitoring
        if 'humidity' in sensor_data:
            humidity = sensor_data['humidity']
            if humidity < self.alert_thresholds['humidity']['min']:
                self.send_alert(
                    'humidity_low',
                    f"Humidity too low: {humidity}% at {timestamp}",
                    priority="medium"
                )
            elif humidity > self.alert_thresholds['humidity']['max']:
                self.send_alert(
                    'humidity_high',
                    f"Humidity too high: {humidity}% at {timestamp}",
                    priority="medium"
                )
        
        # Motion detection
        if 'motion_detected' in sensor_data and sensor_data['motion_detected']:
            if not self.alert_thresholds['motion_detected']:
                self.send_alert(
                    'motion',
                    f"Motion detected in orchard at {timestamp}",
                    priority="high"
                )
                self.alert_thresholds['motion_detected'] = True
        
        # Intrusion detection
        if 'intrusion_detected' in sensor_data and sensor_data['intrusion_detected']:
            if not self.alert_thresholds['intrusion_detected']:
                self.send_alert(
                    'intrusion',
                    f"🚨 INTRUSION DETECTED in orchard at {timestamp}!",
                    priority="high"
                )
                self.alert_thresholds['intrusion_detected'] = True
    
    def reset_alerts(self):
        """Reset alert states"""
        self.alert_thresholds['motion_detected'] = False
        self.alert_thresholds['intrusion_detected'] = False
    
    def send_daily_report(self):
        """Send daily status report"""
        message = f"📊 Daily FruitGuard Report - {datetime.now().strftime('%Y-%m-%d')}\n"
        message += "All systems operational. No critical alerts."
        
        self.send_alert('daily_report', message, priority="normal")

# Example usage
if __name__ == '__main__':
    # Initialize FruitGuard IoT
    fruitguard = FruitGuardIoT()
    
    # Add alert recipients
    fruitguard.add_alert_recipient('1234567890')
    fruitguard.add_alert_recipient('+1234567890')
    
    # Set custom thresholds
    fruitguard.set_alert_thresholds(
        temperature={'min': 10, 'max': 40},
        humidity={'min': 25, 'max': 85}
    )
    
    # Simulate sensor data
    print("Simulating IoT sensor data...")
    
    # Normal conditions
    fruitguard.process_sensor_data({
        'temperature': 25,
        'humidity': 60
    })
    
    time.sleep(2)
    
    # High temperature alert
    fruitguard.process_sensor_data({
        'temperature': 42,
        'humidity': 65
    })
    
    time.sleep(2)
    
    # Motion detection
    fruitguard.process_sensor_data({
        'temperature': 28,
        'humidity': 58,
        'motion_detected': True
    })
    
    time.sleep(2)
    
    # Intrusion alert
    fruitguard.process_sensor_data({
        'temperature': 30,
        'humidity': 55,
        'intrusion_detected': True
    })
    
    time.sleep(2)
    
    # Daily report
    fruitguard.send_daily_report()
    
    print("IoT simulation completed!")

