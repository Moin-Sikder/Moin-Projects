# 🏦 Personalized Offer Engine API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An intelligent, AI-powered API that provides personalized banking product recommendations based on customer profiles, financial behavior, and eligibility criteria. Designed for private banks to enhance cross-selling and customer engagement strategies.

## 📊 Business Value Proposition

**Bridge the gap between marketing strategy and technical execution** by providing data-driven product recommendations that:
- Increase cross-selling success rates by 30%+
- Enhance customer experience through personalized offers
- Optimize marketing campaign ROI through targeted suggestions
- Reduce customer acquisition costs through intelligent segmentation

## 🚀 Features

### Core Capabilities
- **🤖 Smart Recommendation Engine**: Advanced algorithm considering multiple customer dimensions
- **🎯 Confidence Scoring**: Each recommendation includes a 0-100% confidence score
- **📊 Customer Segmentation**: Automatic categorization based on financial profile
- **⚡ Real-time Processing**: Instant recommendations via RESTful API
- **🔒 Data Validation**: Robust input validation using Pydantic models

### Business Intelligence
- **Income-based Targeting** - Product matching based on earning capacity
- **Credit Profile Analysis** - Risk-adjusted recommendations
- **Product Gap Analysis** - Identifies missing products in customer portfolio
- **Behavioral Scoring** - Considers spending and saving patterns

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | FastAPI | High-performance web framework with automatic docs |
| **Validation** | Pydantic | Data validation using Python type hints |
| **Server** | Uvicorn | ASGI server for production deployment |
| **Language** | Python 3.7+ | Core programming language |

## 📥 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step-by-Step Installation

**1. Create Virtual Environment (Recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**2. Install Dependencies**

```bash
pip install -r requirements.txt
```

**3. Launch the API Server**

```bash
python app.py
```

**4. Verify Installation**
   · API will be running at: http://localhost:8000
   · Interactive documentation: http://localhost:8000/docs
   · Alternative docs: http://localhost:8000/redoc

## 🎯 API Endpoints

1. Get Product Recommendations

Endpoint: GET /recommend/{customer_id}

Get personalized product recommendations for existing customers.

Example Request:

```http
GET http://localhost:8000/recommend/C001
```

Example Response:

```json
{
  "customer_id": "C001",
  "recommended_products": [
    {
      "product_name": "Premium Credit Card",
      "category": "credit",
      "reason": "High income and good credit score",
      "confidence_score": 85.5
    },
    {
      "product_name": "Investment Account", 
      "category": "investment",
      "reason": "Good savings potential",
      "confidence_score": 72.3
    }
  ],
  "total_recommendations": 2
}
```

2. Custom Customer Recommendations

Endpoint: POST /recommend/

Get recommendations for custom customer data (ideal for new customers).

Example Request:

```http
POST http://localhost:8000/recommend/
Content-Type: application/json

{
  "customer_id": "NEW001",
  "age": 32,
  "income": 85000,
  "existing_products": ["savings_account", "debit_card"],
  "credit_score": 710,
  "avg_account_balance": 25000
}
```

3. View All Customers

Endpoint: GET /customers

Retrieve all mock customer profiles for testing.

4. View Available Products

Endpoint: GET /products

Get complete list of bank products with eligibility criteria.

### 🧠 Recommendation Algorithm

Scoring Dimensions

The algorithm evaluates customers across multiple dimensions:

Dimension Weight Description
Income Level 40% Compares customer income against product minimums
Credit Score 30% Assesses creditworthiness and risk profile
Account Balance 20% Evaluates savings and investment capacity
Age Eligibility 10% Ensures regulatory compliance

Business Rules

* **Exclusion Logic**: Won't recommend products customer already owns
* **Confidence Threshold**: Only suggests products with >30% confidence
* **Risk Adjustment**: Higher credit requirements for premium products
* **Portfolio Gaps**: Identifies missing product categories

## 💼 Business Use Cases

### For Private Banks

Use Case Benefit API Endpoint
Digital Onboarding Suggest starter products for new customers POST /recommend/
Relationship Manager Tool Assist RM in customer meetings GET /recommend/{id}
Campaign Targeting Identify customers for marketing campaigns Batch processing
Product Development Understand customer needs and gaps Analytics from recommendations

### For Marketing Teams

* **Segmented Campaigns**: Target specific customer segments with relevant offers
* **Personalized Communication**: Tailor messaging based on recommended products
* **Performance Tracking**: Monitor recommendation-to-conversion rates
* **Customer Lifecycle Management**: Progressive product adoption strategies

### 📋 Sample Customer Segments

Segment Profile Typical Recommendations
Young Professionals Age 22-30, Income $40-70K Credit Cards, Personal Loans, Basic Investments
Affluent Customers Income $100K+, High Balances Premium Cards, Wealth Management, Investment Accounts
Retirement Planners Age 45+, Stable Income Retirement Accounts, Fixed Deposits, Insurance
Credit Builders Low Credit Score, Steady Income Secured Cards, Gold Loans, Savings Products

### 🔧 Integration Examples

Python Client

```python
import requests

def get_recommendations(customer_id):
    response = requests.get(f"http://localhost:8000/recommend/{customer_id}")
    return response.json()

# Usage
recommendations = get_recommendations("C001")
for product in recommendations['recommended_products']:
    print(f"📦 {product['product_name']} - Confidence: {product['confidence_score']}%")
    print(f"   💡 Reason: {product['reason']}")
```

cURL Example

```bash
curl -X GET "http://localhost:8000/recommend/C001" -H "Content-Type: application/json"
```

JavaScript Fetch

```javascript
async function fetchRecommendations(customerId) {
    const response = await fetch(`http://localhost:8000/recommend/${customerId}`);
    const data = await response.json();
    return data;
}
```

## 🗂️ Project Structure

```
offer-engine-api/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── mock_data.py          # Sample customer and product data
├── README.md             # This documentation
└── .gitignore           # Git ignore rules
```

### 🚀 Deployment Options

Local Development

```bash
python app.py
```

Production with Uvicorn

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

📈 Extending the API

Adding New Products

Edit mock_data.py to include new banking products:

```python
new_product = {
    "business_loan": {
        "name": "Business Expansion Loan",
        "min_income": 80000,
        "min_credit_score": 680,
        "min_age": 25,
        "reason": "Strong income potential for business growth",
        "category": "commercial_loan"
    }
}
```

Custom Scoring Logic

Modify the calculate_confidence() function in app.py to incorporate additional factors like:

* Transaction history patterns
* Customer lifetime value
* Geographic location
* Market segment trends

## 🤝 Contributing

We welcome contributions from the community! Please feel free to:

* Report bugs and issues
* Suggest new features and enhancements
* Submit pull requests
* Improve documentation

## 🙏 Acknowledgments

* Built with FastAPI for high-performance APIs
* Inspired by real-world banking recommendation systems
* Designed for BBA Marketing graduates entering fintech sector

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
