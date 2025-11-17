from datetime import datetime, timedelta
from models import Subscription

def calculate_upcoming_costs(subscriptions):
    """Calculate total upcoming monthly and yearly costs"""
    monthly_total = 0
    yearly_total = 0
    
    for sub in subscriptions:
        if sub.status == 'active':
            yearly_total += sub.calculate_yearly_cost()
            if sub.frequency == 'monthly':
                monthly_total += sub.amount
            elif sub.frequency == 'weekly':
                monthly_total += sub.amount * 4
            elif sub.frequency == 'yearly':
                # For monthly display, divide yearly by 12
                monthly_total += sub.amount / 12
    
    return {
        'monthly_total': round(monthly_total, 2),
        'yearly_total': round(yearly_total, 2)
    }

def get_subscriptions_by_category(subscriptions):
    """Group subscriptions by category"""
    categories = {}
    for sub in subscriptions:
        if sub.status == 'active':
            category = sub.category or 'Uncategorized'
            if category not in categories:
                categories[category] = []
            categories[category].append(sub.to_dict())
    return categories