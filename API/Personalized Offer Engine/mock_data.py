# Mock customer and product data
mock_customers = [
    {
        "customer_id": "C001",
        "age": 28,
        "income": 75000,
        "existing_products": ["savings_account", "debit_card"],
        "credit_score": 720,
        "avg_account_balance": 15000
    },
    {
        "customer_id": "C002", 
        "age": 45,
        "income": 120000,
        "existing_products": ["savings_account", "credit_card", "home_loan"],
        "credit_score": 680,
        "avg_account_balance": 45000
    },
    {
        "customer_id": "C003",
        "age": 22,
        "income": 35000,
        "existing_products": ["savings_account"],
        "credit_score": 650,
        "avg_account_balance": 5000
    }
]

bank_products = {
    "premium_credit_card": {
        "name": "Premium Credit Card",
        "min_income": 60000,
        "min_credit_score": 700,
        "min_age": 21,
        "reason": "High income and good credit score",
        "category": "credit"
    },
    "personal_loan": {
        "name": "Personal Loan", 
        "min_income": 40000,
        "min_credit_score": 650,
        "min_age": 23,
        "reason": "Stable income and decent credit history",
        "category": "loan"
    },
    "investment_account": {
        "name": "Investment Account",
        "min_income": 50000,
        "min_credit_score": 0,
        "min_age": 18,
        "reason": "Good savings potential",
        "category": "investment"
    },
    "car_loan": {
        "name": "Auto Loan",
        "min_income": 30000,
        "min_credit_score": 620,
        "min_age": 21,
        "reason": "Eligible for vehicle financing",
        "category": "loan"
    },
    "gold_loan": {
        "name": "Gold Loan",
        "min_income": 20000,
        "min_credit_score": 550,
        "min_age": 21,
        "reason": "Quick access to funds against gold",
        "category": "loan"
    }
}