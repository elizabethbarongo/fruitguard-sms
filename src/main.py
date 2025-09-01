from flask import Flask, request, jsonify
from config import Config
from services.smsleopard_service import SMSLeopardService
from utils.logger import setup_logger
import json

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
sms_service = SMSLeopardService()
logger = setup_logger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'fruitguard-sms',
        'version': '1.0.0'
    }), 200

@app.route('/sms/send', methods=['POST'])
def send_sms():
    """Send SMS endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['phone_numbers', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        phone_numbers = data['phone_numbers']
        message = data['message']
        sender_id = data.get('sender_id')
        schedule_time = data.get('schedule_time')
        
        # Validate phone numbers
        if not isinstance(phone_numbers, list) or not phone_numbers:
            return jsonify({'error': 'phone_numbers must be a non-empty list'}), 400
        
        # Format phone numbers
        formatted_numbers = sms_service.format_phone_numbers(phone_numbers)
        if not formatted_numbers:
            return jsonify({'error': 'No valid phone numbers provided'}), 400
        
        # Send SMS
        result = sms_service.send_sms_with_retry(
            phone_numbers=formatted_numbers,
            message=message,
            sender_id=sender_id,
            max_retries=data.get('max_retries')
        )
        
        logger.info(f"SMS sent successfully via API endpoint")
        return jsonify({
            'success': True,
            'message': 'SMS sent successfully',
            'data': result
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/sms/status/<message_id>', methods=['GET'])
def get_sms_status(message_id):
    """Get SMS status endpoint"""
    try:
        if not message_id:
            return jsonify({'error': 'Message ID is required'}), 400
        
        result = sms_service.get_sms_status(message_id)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting SMS status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/account/balance', methods=['GET'])
def get_balance():
    """Get account balance endpoint"""
    try:
        result = sms_service.get_balance()
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting balance: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/sms/validate', methods=['POST'])
def validate_phone_numbers():
    """Validate phone numbers endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'phone_numbers' not in data:
            return jsonify({'error': 'phone_numbers field is required'}), 400
        
        phone_numbers = data['phone_numbers']
        if not isinstance(phone_numbers, list):
            return jsonify({'error': 'phone_numbers must be a list'}), 400
        
        validation_results = {}
        for number in phone_numbers:
            validation_results[number] = sms_service.validate_phone_number(number)
        
        formatted_numbers = sms_service.format_phone_numbers(phone_numbers)
        
        return jsonify({
            'success': True,
            'validation_results': validation_results,
            'formatted_numbers': formatted_numbers
        }), 200
        
    except Exception as e:
        logger.error(f"Error validating phone numbers: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/dr', methods=['POST'])
def delivery_report():
    """Delivery report webhook endpoint (following original format)"""
    logger.info("=== Delivery Report Callback ===")
    logger.info(f"Headers: {dict(request.headers)}")
    
    payload = request.get_json(silent=True)
    logger.info(f"JSON: {payload}")
    
    # Process delivery report
    if payload:
        try:
            # Extract relevant information from payload
            message_id = payload.get('message_id')
            status = payload.get('status')
            recipient = payload.get('to')
            
            logger.info(f"Message ID: {message_id}, Status: {status}, Recipient: {recipient}")
            
            # Here you can add logic to store delivery status in database
            # or trigger other actions based on delivery status
            
        except Exception as e:
            logger.error(f"Error processing delivery report: {str(e)}")
    
    return ("", 204)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info(f"Starting FruitGuard SMS service on {Config.HOST}:{Config.PORT}")
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

