from main import Transaction, AnalysisRequest

def get_sample_data():
    """
    Generate sample transaction data for testing
    """
    return AnalysisRequest(
        transactions=[
            Transaction(id=1, description="Starbucks Coffee", amount=5.75, date="2024-01-15"),
            Transaction(id=2, description="Amazon Purchase", amount=89.99, date="2024-01-16"),
            Transaction(id=3, description="Shell Gas Station", amount=45.50, date="2024-01-16"),
            Transaction(id=4, description="Netflix Subscription", amount=15.99, date="2024-01-17"),
            Transaction(id=5, description="Walmart Groceries", amount=125.30, date="2024-01-18"),
            Transaction(id=6, description="Uber Ride", amount=23.45, date="2024-01-19"),
            Transaction(id=7, description="Pizza Hut", amount=32.15, date="2024-01-20"),
            Transaction(id=8, description="Apple Store", amount=299.99, date="2024-01-21"),
            Transaction(id=9, description="Electricity Bill", amount: 85.00, date="2024-01-22"),
            Transaction(id=10, description="CVS Pharmacy", amount: 28.75, date="2024-01-23"),
        ]
    )

# Example of how to test the API
if __name__ == "__main__":
    from main import analyze_spending_patterns
    
    sample_data = get_sample_data()
    result = analyze_spending_patterns(sample_data.transactions)
    
    print("=== SPENDING ANALYSIS RESULTS ===")
    print(f"Total Spent: ${result.total_spent}")
    print(f"Transactions: {result.transaction_count}")
    print("\n=== CATEGORY BREAKDOWN ===")
    for category in result.category_breakdown:
        print(f"{category.category}: ${category.total_amount} ({category.percentage}%)")
    print("\n=== INSIGHTS ===")
    for insight in result.insights:
        print(f"• {insight}")