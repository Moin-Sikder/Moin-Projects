use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ClickEvent {
    pub campaign_id: String,
    pub user_id: String,
    pub timestamp: DateTime<Utc>,
    pub ip_address: String,
    pub user_agent: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct CampaignStats {
    pub total_clicks: u64,
    pub unique_users: std::collections::HashSet<String>,
    pub click_timestamps: Vec<DateTime<Utc>>,
}

#[derive(Debug, Clone, Serialize)]
pub struct AggregationResult {
    pub campaign_id: String,
    pub total_clicks: u64,
    pub unique_users: usize,
    pub clicks_per_second: f64,
}
