from flask import Blueprint, request, jsonify
from models import db, Subscription, Transaction
from utils.helpers import calculate_upcoming_costs, get_subscriptions_by_category
from datetime import datetime, timedelta
import json

subscriptions_bp = Blueprint('subscriptions', __name__)

@subscriptions_bp.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    """Get all subscriptions for a user"""
    user_id = request.args.get('user_id', 'default_user')
    
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    
    # Calculate totals
    totals = calculate_upcoming_costs(subscriptions)
    categories = get_subscriptions_by_category(subscriptions)
    
    return jsonify({
        'subscriptions': [sub.to_dict() for sub in subscriptions],
        'totals': totals,
        'categories': categories
    })

@subscriptions_bp.route('/subscriptions', methods=['POST'])
def create_subscription():
    """Create a new subscription"""
    data = request.get_json()
    
    try:
        subscription = Subscription(
            name=data['name'],
            amount=data['amount'],
            currency=data.get('currency', 'USD'),
            frequency=data['frequency'],
            next_billing_date=datetime.strptime(data['next_billing_date'], '%Y-%m-%d').date(),
            category=data.get('category', 'Other'),
            user_id=data.get('user_id', 'default_user')
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({
            'message': 'Subscription created successfully',
            'subscription': subscription.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@subscriptions_bp.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    """Update a subscription"""
    subscription = Subscription.query.get_or_404(subscription_id)
    data = request.get_json()
    
    try:
        subscription.name = data.get('name', subscription.name)
        subscription.amount = data.get('amount', subscription.amount)
        subscription.frequency = data.get('frequency', subscription.frequency)
        subscription.category = data.get('category', subscription.category)
        subscription.status = data.get('status', subscription.status)
        
        if 'next_billing_date' in data:
            subscription.next_billing_date = datetime.strptime(data['next_billing_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Subscription updated successfully',
            'subscription': subscription.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@subscriptions_bp.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    """Delete a subscription"""
    subscription = Subscription.query.get_or_404(subscription_id)
    
    db.session.delete(subscription)
    db.session.commit()
    
    return jsonify({'message': 'Subscription deleted successfully'})

@subscriptions_bp.route('/analytics/monthly-spending', methods=['GET'])
def monthly_spending_analytics():
    """Get monthly spending analytics"""
    user_id = request.args.get('user_id', 'default_user')
    
    subscriptions = Subscription.query.filter_by(user_id=user_id, status='active').all()
    
    # Calculate spending by category
    category_spending = {}
    for sub in subscriptions:
        category = sub.category or 'Uncategorized'
        monthly_cost = sub.amount
        if sub.frequency == 'yearly':
            monthly_cost = sub.amount / 12
        elif sub.frequency == 'weekly':
            monthly_cost = sub.amount * 4
        
        if category not in category_spending:
            category_spending[category] = 0
        category_spending[category] += monthly_cost
    
    # Round the values
    for category in category_spending:
        category_spending[category] = round(category_spending[category], 2)
    
    return jsonify({
        'monthly_spending_by_category': category_spending,
        'total_monthly_spending': round(sum(category_spending.values()), 2)
    })

@subscriptions_bp.route('/subscriptions/upcoming-renewals', methods=['GET'])
def upcoming_renewals():
    """Get subscriptions due for renewal in the next 7 days"""
    user_id = request.args.get('user_id', 'default_user')
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    upcoming = Subscription.query.filter(
        Subscription.user_id == user_id,
        Subscription.status == 'active',
        Subscription.next_billing_date >= today,
        Subscription.next_billing_date <= next_week
    ).all()
    
    return jsonify({
        'upcoming_renewals': [sub.to_dict() for sub in upcoming],
        'period': f'{today} to {next_week}'
    })