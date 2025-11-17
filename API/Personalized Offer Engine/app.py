from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mock_data

app = FastAPI(
    title="Personalized Offer Engine API",
    description="AI-powered banking product recommendations based on customer profile",
    version="1.0.0"
)

class CustomerProfile(BaseModel):
    customer_id: str
    age: int
    income: float
    existing_products: List[str]
    credit_score: int
    avg_account_balance: float

class ProductRecommendation(BaseModel):
    product_name: str
    category: str
    reason: str
    confidence_score: float

class RecommendationResponse(BaseModel):
    customer_id: str
    recommended_products: List[ProductRecommendation]
    total_recommendations: int

def calculate_confidence(customer, product):
    """Calculate confidence score for product recommendation"""
    score = 0
    max_score = 100
    
    # Income factor (40%)
    income_ratio = min(customer['income'] / product['min_income'], 2.0)
    score += (income_ratio - 1) * 40
    
    # Credit score factor (30%)
    if product['min_credit_score'] > 0:
        credit_ratio = min(customer['credit_score'] / product['min_credit_score'], 1.5)
        score += (credit_ratio - 1) * 30
    
    # Account balance factor (20%)
    balance_ratio = min(customer['avg_account_balance'] / 10000, 3.0)
    score += (balance_ratio - 1) * 20
    
    # Age factor (10%)
    if customer['age'] >= product['min_age']:
        score += 10
    
    return max(0, min(score, 100))

def get_recommendations(customer_data):
    """Generate product recommendations based on customer profile"""
    recommendations = []
    
    for product_id, product in mock_data.bank_products.items():
        # Check basic eligibility
        if (customer_data['age'] >= product['min_age'] and 
            customer_data['income'] >= product['min_income'] and 
            customer_data['credit_score'] >= product['min_credit_score']):
            
            # Check if customer already has this product type
            product_owned = any(product['category'] in prod for prod in customer_data['existing_products'])
            
            if not product_owned:
                confidence = calculate_confidence(customer_data, product)
                
                if confidence > 30:  # Minimum confidence threshold
                    recommendations.append(ProductRecommendation(
                        product_name=product['name'],
                        category=product['category'],
                        reason=product['reason'],
                        confidence_score=round(confidence, 2)
                    ))
    
    # Sort by confidence score (highest first)
    recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
    return recommendations

@app.get("/")
async def root():
    return {"message": "Personalized Offer Engine API", "status": "active"}

@app.get("/customers", response_model=List[dict])
async def get_all_customers():
    """Get all mock customer data"""
    return mock_data.mock_customers

@app.get("/recommend/{customer_id}", response_model=RecommendationResponse)
async def recommend_products(customer_id: str):
    """Get product recommendations for a specific customer"""
    customer = next((c for c in mock_data.mock_customers if c['customer_id'] == customer_id), None)
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    recommendations = get_recommendations(customer)
    
    return RecommendationResponse(
        customer_id=customer_id,
        recommended_products=recommendations,
        total_recommendations=len(recommendations)
    )

@app.post("/recommend/", response_model=RecommendationResponse)
async def recommend_products_custom(customer: CustomerProfile):
    """Get product recommendations for custom customer data"""
    customer_data = customer.dict()
    recommendations = get_recommendations(customer_data)
    
    return RecommendationResponse(
        customer_id=customer_data['customer_id'],
        recommended_products=recommendations,
        total_recommendations=len(recommendations)
    )

@app.get("/products")
async def get_all_products():
    """Get all available bank products"""
    return mock_data.bank_products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)