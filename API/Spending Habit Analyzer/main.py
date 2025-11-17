from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime
import re

app = FastAPI(
    title="Spending Habit Analyzer API",
    description="Analyze transaction data to provide spending insights and categorization",
    version="1.0.0"
)

# Transaction data model
class Transaction(BaseModel):
    id: int
    description: str
    amount: float
    date: str
    category: Optional[str] = None

class AnalysisRequest(BaseModel):
    transactions: List[Transaction]

class CategorySummary(BaseModel):
    category: str
    total_amount: float
    transaction_count: int
    percentage: float

class AnalysisResponse(BaseModel):
    total_spent: float
    transaction_count: int
    category_breakdown: List[CategorySummary]
    monthly_trend: Dict[str, float]
    insights: List[str]

# Category mapping based on keywords
CATEGORY_KEYWORDS = {
    'Food & Dining': ['mcdonalds', 'kfc', 'restaurant', 'cafe', 'pizza', 'burger', 'starbucks', 'food', 'dining', 'eat'],
    'Shopping': ['mall', 'shop', 'store', 'amazon', 'flipkart', 'myntra', 'zara', 'h&m', 'purchase'],
    'Entertainment': ['netflix', 'movie', 'cinema', 'theater', 'spotify', 'game', 'concert'],
    'Transportation': ['uber', 'ola', 'taxi', 'bus', 'metro', 'fuel', 'petrol', 'diesel', 'transport'],
    'Utilities': ['electricity', 'water', 'internet', 'wifi', 'mobile', 'phone', 'bill'],
    'Healthcare': ['hospital', 'clinic', 'doctor', 'medical', 'pharmacy', 'medicine'],
    'Groceries': ['grocery', 'supermarket', 'vegetable', 'fruit', 'milk', 'bread'],
    'Transfer': ['transfer', 'send', 'received', 'payment'],
    'Other': []
}

def categorize_transaction(description: str) -> str:
    desc_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in desc_lower for keyword in keywords):
            return category
    return 'Other'

def analyze_spending_patterns(transactions: List[Transaction]) -> AnalysisResponse:
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame([t.dict() for t in transactions])
    
    # Add categories if not present
    if 'category' not in df.columns or df['category'].isna().any():
        df['category'] = df['description'].apply(categorize_transaction)
    
    # Calculate total spending
    total_spent = df['amount'].sum()
    
    # Category breakdown
    category_stats = df.groupby('category').agg({
        'amount': ['sum', 'count']
    }).round(2)
    
    category_breakdown = []
    for category, ((total_amount, transaction_count),) in category_stats.iterrows():
        percentage = round((total_amount / total_spent) * 100, 2) if total_spent > 0 else 0
        category_breakdown.append(CategorySummary(
            category=category,
            total_amount=round(total_amount, 2),
            transaction_count=int(transaction_count),
            percentage=percentage
        ))
    
    # Monthly trend (simplified - using last 3 characters as month identifier)
    monthly_trend = {}
    try:
        df['month'] = df['date'].str[-7:]  # Extract MM-YYYY part
        monthly_data = df.groupby('month')['amount'].sum().round(2)
        monthly_trend = monthly_data.to_dict()
    except:
        # Fallback if date parsing fails
        monthly_trend = {"Recent": total_spent}
    
    # Generate insights
    insights = generate_insights(df, total_spent, category_breakdown)
    
    return AnalysisResponse(
        total_spent=round(total_spent, 2),
        transaction_count=len(transactions),
        category_breakdown=category_breakdown,
        monthly_trend=monthly_trend,
        insights=insights
    )

def generate_insights(df: pd.DataFrame, total_spent: float, categories: List[CategorySummary]) -> List[str]:
    insights = []
    
    if total_spent == 0:
        return ["No spending data to analyze"]
    
    # Find top spending category
    top_category = max(categories, key=lambda x: x.total_amount)
    insights.append(f"Your top spending category is {top_category.category} (${top_category.total_amount})")
    
    # Check if food spending is high (>30%)
    food_spending = next((cat for cat in categories if cat.category == 'Food & Dining'), None)
    if food_spending and food_spending.percentage > 30:
        insights.append("💡 Consider reducing dining out expenses - they account for over 30% of your spending")
    
    # Check for large transactions
    large_txns = df[df['amount'] > 500]
    if len(large_txns) > 0:
        insights.append(f"You have {len(large_txns)} large transactions (>$500) this period")
    
    # Savings insight
    if total_spent > 2000:
        insights.append("💰 Your monthly spending is high - consider creating a budget")
    elif total_spent < 500:
        insights.append("👍 Great job keeping your expenses low this month!")
    
    # Multiple small transactions insight
    small_txns = df[df['amount'] < 10]
    if len(small_txns) > 15:
        insights.append("⚠️ You have many small transactions - they can add up quickly!")
    
    return insights

@app.get("/")
async def root():
    return {
        "message": "Spending Habit Analyzer API",
        "endpoints": {
            "analyze": "POST /analyze - Analyze transaction data",
            "categories": "GET /categories - List spending categories",
            "health": "GET /health - API health check"
        }
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_spending(request: AnalysisRequest):
    """
    Analyze transaction data and provide spending insights
    """
    try:
        if not request.transactions:
            raise HTTPException(status_code=400, detail="No transactions provided")
        
        return analyze_spending_patterns(request.transactions)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/categories")
async def get_categories():
    """
    Get list of all spending categories used in analysis
    """
    return {"categories": list(CATEGORY_KEYWORDS.keys())}

@app.get("/health")
async def health_check():
    """
    API health check endpoint
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)