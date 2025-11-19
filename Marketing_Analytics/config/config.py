# config/config.py

class ProjectConfig:
    # Project Settings
    PROJECT_NAME = "Marketing Analytics Dashboard"
    RANDOM_SEED = 42
    
    # Analysis Period (Dynamic Variables)
    START_DATE = '2023-01-01'
    END_DATE = '2024-01-01'
    ANALYSIS_DAYS = 365
    
    # Customer Segmentation Thresholds
    RFM_THRESHOLDS = {
        'recency_days': [30, 90, 180],
        'frequency_bins': [1, 3, 10],
        'monetary_bins': [100, 500, 2000]
    }
    
    # Campaign Performance Metrics
    MIN_CONVERSION_RATE = 0.01
    MAX_COST_PER_ACQUISITION = 100
    
    # Privacy Settings
    ANONYMIZE_IDS = True
    ADD_NOISE_TO_SENSITIVE = True
    NOISE_LEVEL = 0.05
    
    # Database Configuration
    DB_PATH = '/content/marketing_analytics.db'
    
    def update_period(self, start_date, end_date):
        """Update analysis period dynamically"""
        self.START_DATE = start_date
        self.END_DATE = end_date
        
    def update_rfm_thresholds(self, recency, frequency, monetary):
        """Update RFM segmentation thresholds"""
        self.RFM_THRESHOLDS = {
            'recency_days': recency,
            'frequency_bins': frequency,
            'monetary_bins': monetary
        }