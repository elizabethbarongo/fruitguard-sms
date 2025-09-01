import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from src.services.smsleopard_service import SMSLeopardService
from src.main import app

class TestSMSLeopardService(unittest.TestCase):
    """Test cases for SMSLeopardService"""
    
    def setUp(self):
        """Set up test fixtures"""
        with patch('src.services.smsleopard_service.Config') as mock_config:
            mock_config.SMSLEOPARD_API_KEY = 'test_api_key'
            mock_config.SMSLEOPARD_API_URL = 'https://api.smsleopard.com/v1'
            mock_config.DEFAULT_SENDER_ID = 'FruitGuard'
            mock_config.MAX_RETRIES = 3
            mock_config.RETRY_DELAY = 1
            self.sms_service = SMSLeopardService()
    
    def test_validate_phone_number_valid(self):
        """Test phone number validation with valid numbers"""
        valid_numbers = ['+1234567890', '1234567890', '+11234567890']
        
        for number in valid_numbers:
            with self.subTest(number=number):
                self.assertTrue(self.sms_service.validate_phone_number(number))
    
    def test_validate_phone_number_invalid(self):
        """Test phone number validation with invalid numbers"""
        invalid_numbers = ['', 'abc', '123', '+', '12345678901234567890']
        
        for number in invalid_numbers:
            with self.subTest(number=number):
                self.assertFalse(self.sms_service.validate_phone_number(number))
    
    def test_format_phone_numbers(self):
        """Test phone number formatting"""
        input_numbers = ['123-456-7890', '+1 234 567 8900', 'invalid']
        expected_formatted = ['1234567890', '12345678900']
        
        formatted = self.sms_service.format_phone_numbers(input_numbers)
        # The actual output shows that 123-456-7890 becomes 1234567890 (cleaned)
        # and +1 234 567 8900 becomes 12345678900 (cleaned)
        self.assertEqual(formatted, expected_formatted)
    
    @patch('requests.post')
    def test_send_sms_success(self, mock_post):
        """Test successful SMS sending"""
        mock_response = Mock()
        mock_response.json.return_value = {'message_id': 'test_id', 'status': 'sent'}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = self.sms_service.send_sms(['1234567890'], 'Test message')
        
        self.assertEqual(result['message_id'], 'test_id')
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_send_sms_failure(self, mock_post):
        """Test SMS sending failure"""
        mock_post.side_effect = Exception('API Error')
        
        with self.assertRaises(Exception):
            self.sms_service.send_sms(['1234567890'], 'Test message')
    
    def test_send_sms_validation_errors(self):
        """Test SMS sending validation errors"""
        # Empty phone numbers
        with self.assertRaises(ValueError):
            self.sms_service.send_sms([], 'Test message')
        
        # Empty message
        with self.assertRaises(ValueError):
            self.sms_service.send_sms(['1234567890'], '')
    
    @patch('requests.get')
    def test_get_sms_status(self, mock_get):
        """Test getting SMS status"""
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'delivered'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.sms_service.get_sms_status('test_id')
        
        self.assertEqual(result['status'], 'delivered')
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_get_balance(self, mock_get):
        """Test getting account balance"""
        mock_response = Mock()
        mock_response.json.return_value = {'balance': 100.50}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.sms_service.get_balance()
        
        self.assertEqual(result['balance'], 100.50)
        mock_get.assert_called_once()

class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application"""
    
    def setUp(self):
        """Set up test fixtures"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'fruitguard-sms')
    
    def test_send_sms_missing_data(self):
        """Test SMS endpoint with missing data"""
        response = self.client.post('/sms/send', 
                                  data=json.dumps({}),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_send_sms_invalid_data(self):
        """Test SMS endpoint with invalid data"""
        test_data = {
            'phone_numbers': 'not_a_list',
            'message': 'Test message'
        }
        
        response = self.client.post('/sms/send', 
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    @patch('src.main.sms_service.send_sms_with_retry')
    def test_send_sms_success(self, mock_send):
        """Test successful SMS sending via API"""
        mock_send.return_value = {'message_id': 'test_id', 'status': 'sent'}
        
        test_data = {
            'phone_numbers': ['1234567890'],
            'message': 'Test message'
        }
        
        response = self.client.post('/sms/send',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        mock_send.assert_called_once()
    
    def test_validate_phone_numbers(self):
        """Test phone number validation endpoint"""
        test_data = {
            'phone_numbers': ['1234567890', 'invalid', '+1234567890']
        }
        
        response = self.client.post('/sms/validate',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('validation_results', data)
        self.assertIn('formatted_numbers', data)
    
    def test_delivery_report_webhook(self):
        """Test delivery report webhook endpoint"""
        test_payload = {
            'message_id': 'test_id',
            'status': 'delivered',
            'to': '+1234567890'
        }
        
        response = self.client.post('/dr',
                                  data=json.dumps(test_payload),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 204)
    
    def test_not_found_error(self):
        """Test 404 error handler"""
        response = self.client.get('/nonexistent')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
