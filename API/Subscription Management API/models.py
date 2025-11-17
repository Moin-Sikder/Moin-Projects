from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    frequency = db.Column(db.String(20), nullable=False)  # monthly, yearly, weekly
    next_billing_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50))  # entertainment, productivity, etc.
    status = db.Column(db.String(20), default='active')
    user_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'currency': self.currency,
            'frequency': self.frequency,
            'next_billing_date': self.next_billing_date.isoformat(),
            'category': self.category,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }
    
    def calculate_yearly_cost(self):
        if self.frequency == 'monthly':
            return self.amount * 12
        elif self.frequency == 'yearly':
            return self.amount
        elif self.frequency == 'weekly':
            return self.amount * 52
        else:
            return self.amount

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='completed')
    
    subscription = db.relationship('Subscription', backref=db.backref('transactions', lazy=True))