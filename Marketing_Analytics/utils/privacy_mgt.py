# utils/privacy_manager.py

import hashlib
import numpy as np
import pandas as pd
from faker import Faker

class PrivacyManager:
    def __init__(self, noise_level=0.05):
        self.fake = Faker()
        self.noise_level = noise_level
        self.customer_mapping = {}
        
    def anonymize_customer_id(self, customer_id):
        """Anonymize customer IDs using hash function"""
        if customer_id not in self.customer_mapping:
            hashed_id = hashlib.sha256(str(customer_id).encode()).hexdigest()[:16]
            self.customer_mapping[customer_id] = f"CUST_{hashed_id}"
        return self.customer_mapping[customer_id]
    
    def add_noise_to_sensitive_data(self, series):
        """Add random noise to sensitive numerical data"""
        noise = np.random.normal(0, self.noise_level * series.std(), len(series))
        return series * (1 + noise)
    
    def generate_fake_demographics(self, n_customers):
        """Generate fake demographic data for privacy"""
        demographics = []
        for i in range(n_customers):
            demographics.append({
                'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '55+']),
                'region': self.fake.state(),
                'signup_channel': np.random.choice(['Organic', 'Paid Search', 'Social Media', 'Email', 'Referral'])
            })
        return pd.DataFrame(demographics)