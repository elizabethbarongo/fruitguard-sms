# FruitGuard SMS Service

A robust SMS messaging service built with Flask and SMSLeopard API for IoT project alerts and notifications, specifically optimized for Kenyan phone numbers.

## Features

- **SMS Sending**: Send SMS messages to multiple recipients with retry mechanism
- **Kenyan Phone Support**: Built-in validation and formatting for Kenyan phone numbers (+254)
- **Delivery Reports**: Webhook endpoint for receiving delivery status updates
- **Phone Validation**: Comprehensive phone number validation and formatting
- **Account Management**: Check account balance and SMS status
- **Error Handling**: Comprehensive error handling and logging
- **Testing**: Complete test suite with unit tests

## Project Structure

```
fruitguard-sms/
├── src/
│   ├── __init__.py
│   ├── main.py              # Flask application
│   ├── config.py            # Configuration management
│   ├── services/
│   │   ├── __init__.py
│   │   └── smsleopard_service.py  # SMSLeopard API service
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # Logging utilities
├── tests/
│   ├── __init__.py
│   └── test_sms.py         # Unit tests
├── status_webhook.py       # Original webhook handler
├── requests.http           # API testing requests
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── test_kenyan_numbers.py # Kenyan phone number testing
├── sms_example.py         # Usage examples
└── README.md              # This file
```

## Prerequisites

- Python 3.8 or higher
- SMSLeopard API account and credentials
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fruitguard-sms
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env file with your actual SMSLeopard credentials
   # SMSLEOPARD_API_KEY=your_actual_api_key
   # SMSLEOPARD_API_SECRET=your_actual_api_secret
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
# SMSLeopard API Configuration
SMSLEOPARD_API_KEY=your_smsleopard_api_key_here
SMSLEOPARD_API_SECRET=your_smsleopard_api_secret_here
SMSLEOPARD_API_URL=https://api.smsleopard.com/v1

# Webhook Configuration
WEBHOOK_SECRET=your_webhook_secret_here
WEBHOOK_ENDPOINT=/dr

# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
DEBUG=False
HOST=0.0.0.0
PORT=5000

# Logging Configuration
LOG_LEVEL=INFO

# SMS Configuration
DEFAULT_SENDER_ID=FruitGuard
MAX_RETRIES=3
RETRY_DELAY=5
```

## Kenyan Phone Number Support

The service is specifically designed to handle Kenyan phone numbers with the following formats:

- `+254712345678` (with +254 prefix)
- `254712345678` (with 254 prefix)
- `0712345678` (with 0 prefix)
- `712345678` (without prefix)

All numbers are automatically formatted to the international format `+254712345678` before sending.

## Running the Application

### Development Mode
```bash
python src/main.py
```

### Production Mode
```bash
# Set DEBUG=False in .env file
python src/main.py
```

The application will start on `http://localhost:5000` (or the configured HOST:PORT).

## API Endpoints

### Health Check
```
GET /health
```
Returns service health status.

### Send SMS
```
POST /sms/send
Content-Type: application/json

{
    "phone_numbers": ["0712345678", "+254712345678", "712345678"],
    "message": "Alert: FruitGuard detected potential threat!",
    "sender_id": "FruitGuard",
    "max_retries": 3,
    "schedule_time": "2024-01-15T08:00:00Z"  // Optional
}
```

### Get SMS Status
```
GET /sms/status/{message_id}
```
Get delivery status of a specific SMS.

### Get Account Balance
```
GET /account/balance
```
Get current account balance.

### Validate Phone Numbers
```
POST /sms/validate
Content-Type: application/json

{
    "phone_numbers": ["0712345678", "invalid", "+254712345678"]
}
```

### Delivery Report Webhook
```
POST /dr
Content-Type: application/json

{
    "message_id": "message_id",
    "status": "delivered",
    "to": "+254712345678",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Testing

### Test Kenyan Phone Numbers
```bash
python test_kenyan_numbers.py
```

### Run All Tests
```bash
python -m unittest discover tests
```

### Run Specific Test File
```bash
python -m unittest tests.test_sms
```

### Run Tests with Coverage
```bash
# Install coverage if not installed
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Generate HTML report
```

## API Testing

Use the provided `requests.http` file to test the API endpoints:

1. **VS Code**: Install "REST Client" extension and open `requests.http`
2. **IntelliJ IDEA**: Open `requests.http` and use the "HTTP Client" feature
3. **Command Line**: Use curl or any HTTP client

Example curl commands:
```bash
# Health check
curl http://localhost:5000/health

# Send SMS to Kenyan number
curl -X POST http://localhost:5000/sms/send \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0712345678"], "message": "Test message"}'
```

## Usage Examples

### Basic SMS Sending
```python
from src.services.smsleopard_service import SMSLeopardService

sms_service = SMSLeopardService()

# Send SMS to Kenyan numbers
result = sms_service.send_sms(
    phone_numbers=['0712345678', '+254712345678'],
    message='Alert: Intrusion detected!'
)
print(f"Message ID: {result.get('message_id')}")
```

### SMS with Retry
```python
# Send with retry mechanism
result = sms_service.send_sms_with_retry(
    phone_numbers=['0712345678'],
    message='Important alert!',
    max_retries=5
)
```

### Phone Number Validation
```python
# Validate Kenyan phone numbers
valid = sms_service.validate_phone_number('+254712345678')
formatted = sms_service.format_phone_numbers(['0712345678', '712345678'])
```

### Run Example Script
```bash
python sms_example.py
```

## Error Handling

The service includes comprehensive error handling:

- **Validation Errors**: Invalid phone numbers, empty messages
- **API Errors**: Network issues, authentication failures
- **Retry Mechanism**: Automatic retry on transient failures
- **Logging**: Detailed logging for debugging

## Logging

Logs are configured with the following levels:
- `INFO`: General application flow
- `WARNING`: Non-critical issues
- `ERROR`: Errors that need attention
- `DEBUG`: Detailed debugging information (when DEBUG=True)

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "src/main.py"]
```

### Environment Variables for Production
- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Configure proper `HOST` and `PORT`
- Set appropriate `LOG_LEVEL`
- Use production SMSLeopard credentials

## Security Considerations

1. **API Key Protection**: Never commit API keys to version control
2. **Webhook Security**: Implement webhook signature verification
3. **Input Validation**: All inputs are validated and sanitized
4. **Rate Limiting**: Consider implementing rate limiting for production
5. **HTTPS**: Use HTTPS in production environments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the logs for error details
2. Verify SMSLeopard API configuration and credentials
3. Test with the provided `requests.http` file
4. Create an issue in the repository