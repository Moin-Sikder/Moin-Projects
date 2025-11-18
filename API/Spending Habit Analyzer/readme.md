# 💰 Spending Habit Analyzer API

A **FastAPI-based REST API** that analyzes transaction data to provide intelligent spending insights and automatic categorization. Perfect for personal finance apps, banking integrations, and financial technology solutions.

## 🌟 Features

### 🔍 Automatic Transaction Categorization
- **Smart Category Detection**: Automatically categorizes transactions into 9 spending categories using keyword matching
- **Customizable Categories**: Easy to extend and modify category definitions
- **Fallback Handling**: Uncategorized transactions are safely grouped as "Other"

### 📊 Comprehensive Spending Analysis
- **Category Breakdown**: Detailed spending distribution across all categories
- **Monthly Trends**: Spending patterns over time with monthly aggregation
- **Total Spending Summary**: Overall expenditure and transaction count

### 💡 Intelligent Insights Generation
- **Behavioral Insights**: AI-powered recommendations based on spending patterns
- **Budgeting Tips**: Personalized suggestions for better financial management
- **Spending Alerts**: Notifications for unusual spending patterns

### 🚀 API Features
- **RESTful Design**: Clean, predictable API endpoints
- **OpenAPI Documentation**: Automatic interactive API documentation
- **JSON Responses**: Consistent and well-structured data format
- **Health Monitoring**: Built-in health check endpoints

## 🛠️ Technology Stack

- **Framework**: FastAPI (Python 3.7+)
- **Data Validation**: Pydantic
- **Data Analysis**: Pandas
- **Server**: Uvicorn (ASGI server)
- **Documentation**: Automatic OpenAPI (Swagger) generation

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step-by-Step Setup

**1. Create Virtual Environment (Recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**2. Install Dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the API Server**

```bash
# Method 1: Using Python directly
python main.py

# Method 2: Using Uvicorn directly (recommended for production)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**4. Verify Installation**
   Open your browser and navigate to:

```
http://localhost:8000/docs
```

You should see the interactive API documentation.

## 🎯 API Endpoints

### 🔍 Analyze Spending

Endpoint: POST /analyze

Analyzes transaction data and returns comprehensive spending insights.

Request Body:

```json
{
  "transactions": [
    {
      "id": 1,
      "description": "Starbucks Coffee",
      "amount": 5.75,
      "date": "2024-01-15"
    },
    {
      "id": 2,
      "description": "Amazon Purchase",
      "amount": 89.99,
      "date": "2024-01-16"
    }
  ]
}
```

Response:

```json
{
  "total_spent": 752.87,
  "transaction_count": 10,
  "category_breakdown": [
    {
      "category": "Food & Dining",
      "total_amount": 38.90,
      "transaction_count": 2,
      "percentage": 5.17
    }
  ],
  "monthly_trend": {
    "2024-01": 752.87
  },
  "insights": [
    "Your top spending category is Shopping ($389.98)",
    "💡 Consider reducing dining out expenses - they account for over 30% of your spending",
    "💰 Your monthly spending is high - consider creating a budget"
  ]
}
```

### 📋 Get Categories

Endpoint: GET /categories

Returns all available spending categories used for transaction classification.

Response:

```json
{
  "categories": [
    "Food & Dining",
    "Shopping",
    "Entertainment",
    "Transportation",
    "Utilities",
    "Healthcare",
    "Groceries",
    "Transfer",
    "Other"
  ]
}
```

### ❤️ Health Check

Endpoint: GET /health

Verifies that the API is running correctly.

Response:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### 🏠 Root Endpoint

Endpoint: GET /

Returns basic API information and available endpoints.

Response:

```json
{
  "message": "Spending Habit Analyzer API",
  "endpoints": {
    "analyze": "POST /analyze - Analyze transaction data",
    "categories": "GET /categories - List spending categories",
    "health": "GET /health - API health check"
  }
}
```

### 📊 Spending Categories

The API automatically categorizes transactions into these categories:

Category Keywords & Examples
Food & Dining Starbucks, McDonald's, restaurant, cafe, pizza, food, dining
Shopping Amazon, Walmart, mall, store, purchase, Zara, H&M
Entertainment Netflix, movie, cinema, Spotify, game, concert
Transportation Uber, taxi, bus, fuel, petrol, gas station
Utilities Electricity, water, internet, phone bill, utility
Healthcare Hospital, clinic, doctor, pharmacy, medical
Groceries Grocery store, supermarket, vegetables, fruits
Transfer Bank transfer, payment sent, money received
Other All uncategorized transactions

### 🧪 Testing the API

Using the Interactive Documentation

1. Start the server
2. Visit http://localhost:8000/docs
3. Click on any endpoint
4. Click "Try it out"
5. Enter the sample data and execute

Using Sample Data

The repository includes mock_data.py with sample transactions:

```python
from mock_data import get_sample_data

# Get sample transaction data
sample_data = get_sample_data()
print(sample_data)
```

Using curl

```bash
curl -X 'POST' \
  'http://localhost:8000/analyze' \
  -H 'Content-Type: application/json' \
  -d '{
  "transactions": [
    {
      "id": 1,
      "description": "Starbucks Coffee",
      "amount": 5.75,
      "date": "2024-01-15"
    }
  ]
}'
```

### 🚀 Deployment

Local Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Production Deployment

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 💡 Business Use Cases

### 🏦 Banking & Financial Institutions

· Customer Spending Insights: Help customers understand their spending patterns
· Personalized Offers: Target marketing based on spending categories
· Budgeting Tools: Integrate with mobile banking apps

### 📱 Personal Finance Apps

· Expense Tracking: Automatic categorization of transactions
· Financial Planning: Data-driven insights for better money management
· Trend Analysis: Monitor spending patterns over time

### 🏢 Enterprise Solutions

· Employee Expense Management: Categorize and analyze corporate spending
· API Integration: Embed spending analytics into existing platforms
· Data Analytics: Aggregate spending data for business intelligence

### 🔧 Customization

Adding New Categories

Edit the CATEGORY_KEYWORDS dictionary in main.py:

```python
CATEGORY_KEYWORDS = {
    'Your New Category': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing categories
}
```

Modifying Insights Logic

Update the generate_insights function in main.py to add custom business rules and recommendations.

Extending Analysis

Add new analysis features by extending the AnalysisResponse model and analyze_spending_patterns function.

### 🐛 Troubleshooting

**Common Issues**

**1. Port already in use**
   ```bash
   uvicorn main:app --port 8001
   ```
**2. Dependencies not installed**
   ```bash
   pip install -r requirements.txt
   ```
3. Python version incompatible
   Ensure you have Python 3.7+ installed

Getting Help

· Check the interactive documentation at /docs
· Review the API logs for error messages
· Verify your request body matches the expected format

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author
**Moin Sikder**

- Co-founder at Zenryse
- Co-founder at 'thereisanapiforthat'
- Expert in Python, bash, Apple Script, Javascript, R
- Expert in Linux-based systems
- Softwares/Tools: Excel, PowerBI, R studio, n8n, Google Colab, Cloud Shell, Docker

--

⭐ ***Don't forget to star*** this repository if you find it helpful!
