# Subscription Management API 💰

A comprehensive **RESTful** API for tracking and managing subscription services with advanced analytics and spending insights. Built with Flask and SQLAlchemy.

## 🌟 Features

- **Subscription CRUD Operations**: Create, read, update, and delete subscriptions
- **Smart Analytics**: Monthly and yearly spending breakdowns
- **Category Management**: Organize subscriptions by categories (Entertainment, Productivity, etc.)
- **Renewal Alerts**: Get notified about upcoming subscription renewals
- **Multi-user Support**: Ready for multiple users with user_id separation
- **RESTful Design**: Clean API endpoints following REST principles
- **CORS Enabled**: Ready for frontend integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

**1. Create virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the application**

```bash
python app.py
```

The API will be available at http://localhost:5000

### 📚 API Documentation

Base URL

```
http://localhost:5000/api
```

Endpoints

### 🏠 Health Check

```http
GET /
```

Response:

```json
{
  "message": "Subscription Management API is running!",
  "status": "success",
  "endpoints": {
    "get_subscriptions": "GET /api/subscriptions?user_id=user_id",
    "create_subscription": "POST /api/subscriptions",
    "monthly_analytics": "GET /api/analytics/monthly-spending?user_id=user_id",
    "upcoming_renewals": "GET /api/subscriptions/upcoming-renewals?user_id=user_id"
  }
}
```

### 📋 Get All Subscriptions

```http
GET /subscriptions?user_id={user_id}
```

Parameters:

· user_id (required): User identifier

Response:

```json
{
  "subscriptions": [
    {
      "id": 1,
      "name": "Netflix",
      "amount": 15.99,
      "currency": "USD",
      "frequency": "monthly",
      "next_billing_date": "2024-01-15",
      "category": "Entertainment",
      "status": "active",
      "user_id": "user123",
      "created_at": "2024-01-01T10:00:00"
    }
  ],
  "totals": {
    "monthly_total": 45.97,
    "yearly_total": 551.64
  },
  "categories": {
    "Entertainment": [...],
    "Productivity": [...]
  }
}
```

### ➕ Create Subscription

```http
POST /subscriptions
Content-Type: application/json
```

Request Body:

```json
{
  "name": "Spotify Premium",
  "amount": 9.99,
  "frequency": "monthly",
  "next_billing_date": "2024-01-20",
  "category": "Music",
  "user_id": "user123"
}
```

Optional Fields:

· currency (default: "USD")
· status (default: "active")

Response:

```json
{
  "message": "Subscription created successfully",
  "subscription": {
    "id": 2,
    "name": "Spotify Premium",
    "amount": 9.99,
    "currency": "USD",
    "frequency": "monthly",
    "next_billing_date": "2024-01-20",
    "category": "Music",
    "status": "active",
    "user_id": "user123",
    "created_at": "2024-01-01T10:00:00"
  }
}
```

### ✏️ Update Subscription

```http
PUT /subscriptions/{id}
Content-Type: application/json
```

Request Body:

```json
{
  "name": "Netflix Premium",
  "amount": 19.99,
  "status": "cancelled"
}
```

### 🗑️ Delete Subscription

```http
DELETE /subscriptions/{id}
```

### 📊 Monthly Spending Analytics

```http
GET /analytics/monthly-spending?user_id={user_id}
```

Response:

```json
{
  "monthly_spending_by_category": {
    "Entertainment": 25.98,
    "Productivity": 19.99,
    "Music": 9.99
  },
  "total_monthly_spending": 55.96
}
```

### 🔔 Upcoming Renewals

```http
GET /subscriptions/upcoming-renewals?user_id={user_id}
```

Response:

```json
{
  "upcoming_renewals": [
    {
      "id": 1,
      "name": "Netflix",
      "amount": 15.99,
      "next_billing_date": "2024-01-15",
      "category": "Entertainment"
    }
  ],
  "period": "2024-01-08 to 2024-01-15"
}
```

## 🛠️ Project Structure

```
subscription-management-api/
├── app.py                 # Main application entry point
├── config.py             # Configuration settings
├── models.py             # Database models (Subscription, Transaction)
├── requirements.txt      # Python dependencies
├── routes/
│   └── subscriptions.py  # API route handlers
└── utils/
    └── helpers.py        # Utility functions and calculations
```

### 📊 Usage Examples

Python Client Example

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Create a subscription
subscription_data = {
    "name": "Adobe Creative Cloud",
    "amount": 52.99,
    "frequency": "monthly",
    "next_billing_date": "2024-02-01",
    "category": "Productivity",
    "user_id": "user123"
}

response = requests.post(f"{BASE_URL}/subscriptions", json=subscription_data)
print(response.json())

# Get monthly analytics
analytics = requests.get(f"{BASE_URL}/analytics/monthly-spending?user_id=user123")
print(analytics.json())
```

cURL Examples

Create Subscription:

```bash
curl -X POST http://localhost:5000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Netflix",
    "amount": 15.99,
    "frequency": "monthly",
    "next_billing_date": "2024-01-15",
    "category": "Entertainment",
    "user_id": "user123"
  }'
```

Get Analytics:

```bash
curl "http://localhost:5000/api/analytics/monthly-spending?user_id=user123"
```

### 🔧 Configuration

Environment Variables

Create a .env file for configuration:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///subscriptions.db
DEBUG=True
```

Database

The application uses SQLite by default. To use PostgreSQL or MySQL, update the DATABASE_URL in config.py:

```python
# PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/database'

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/database'
```

### 🧪 Testing

Manual Testing with Postman

1. Import the following collection into Postman:

```json
{
  "variables": [],
  "info": {
    "name": "Subscription API",
    "description": "",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Subscription",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Netflix\",\n  \"amount\": 15.99,\n  \"frequency\": \"monthly\",\n  \"next_billing_date\": \"2024-01-15\",\n  \"category\": \"Entertainment\",\n  \"user_id\": \"test_user\"\n}"
        },
        "url": {
          "raw": "http://localhost:5000/api/subscriptions",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "subscriptions"]
        }
      }
    }
  ]
}
```

### 🚀 Deployment

Local Development

```bash
python app.py
```

Production with Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

Docker Deployment

Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t subscription-api .
docker run -p 5000:5000 subscription-api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

· Flask community for the excellent web framework
· SQLAlchemy for ORM capabilities
· Open source contributors

---

# 👨‍💻 Author

**Moin Sikder**

· GitHub: @Moin-Sikder
· LinkedIn: Moin Sikder

--

⭐ Don't forget to star this repository if you find it helpful!