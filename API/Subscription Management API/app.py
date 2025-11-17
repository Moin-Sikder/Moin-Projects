from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from routes.subscriptions import subscriptions_bp
from config import DevelopmentConfig
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(subscriptions_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Health check route
    @app.route('/')
    def health_check():
        return jsonify({
            'message': 'Subscription Management API is running!',
            'status': 'success',
            'endpoints': {
                'get_subscriptions': 'GET /api/subscriptions?user_id=user_id',
                'create_subscription': 'POST /api/subscriptions',
                'monthly_analytics': 'GET /api/analytics/monthly-spending?user_id=user_id',
                'upcoming_renewals': 'GET /api/subscriptions/upcoming-renewals?user_id=user_id'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)