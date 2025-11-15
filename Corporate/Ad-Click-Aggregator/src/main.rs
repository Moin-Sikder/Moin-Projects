use axum::{
    extract::State,
    http::StatusCode,
    response::Json,
    routing::post,
    Router,
};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use uuid::Uuid;

type ClickStorage = Arc<RwLock<HashMap<String, CampaignStats>>>;

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

#[derive(Debug, Clone)]
pub struct AppState {
    pub storage: ClickStorage,
}

impl AppState {
    pub fn new() -> Self {
        Self {
            storage: Arc::new(RwLock::new(HashMap::new())),
        }
    }
}

async fn record_click(
    State(state): State<Arc<AppState>>,
    Json(click): Json<ClickEvent>,
) -> Result<Json<AggregationResult>, StatusCode> {
    let mut storage = state.storage.write().await;
    
    let stats = storage.entry(click.campaign_id.clone()).or_default();
    
    // Update statistics
    stats.total_clicks += 1;
    stats.unique_users.insert(click.user_id.clone());
    stats.click_timestamps.push(click.timestamp);
    
    // Calculate clicks per second (simplified)
    let clicks_per_second = if stats.click_timestamps.len() > 1 {
        let first = stats.click_timestamps.first().unwrap();
        let last = stats.click_timestamps.last().unwrap();
        let duration = last.signed_duration_since(*first);
        stats.click_timestamps.len() as f64 / duration.num_seconds().max(1) as f64
    } else {
        0.0
    };
    
    let result = AggregationResult {
        campaign_id: click.campaign_id.clone(),
        total_clicks: stats.total_clicks,
        unique_users: stats.unique_users.len(),
        clicks_per_second,
    };
    
    Ok(Json(result))
}

async fn get_campaign_stats(
    State(state): State<Arc<AppState>>,
    axum::extract::Path(campaign_id): axum::extract::Path<String>,
) -> Result<Json<AggregationResult>, StatusCode> {
    let storage = state.storage.read().await;
    
    if let Some(stats) = storage.get(&campaign_id) {
        let clicks_per_second = if stats.click_timestamps.len() > 1 {
            let first = stats.click_timestamps.first().unwrap();
            let last = stats.click_timestamps.last().unwrap();
            let duration = last.signed_duration_since(*first);
            stats.click_timestamps.len() as f64 / duration.num_seconds().max(1) as f64
        } else {
            0.0
        };
        
        let result = AggregationResult {
            campaign_id: campaign_id.clone(),
            total_clicks: stats.total_clicks,
            unique_users: stats.unique_users.len(),
            clicks_per_second,
        };
        
        Ok(Json(result))
    } else {
        Err(StatusCode::NOT_FOUND)
    }
}

async fn get_all_stats(
    State(state): State<Arc<AppState>>,
) -> Json<HashMap<String, CampaignStats>> {
    let storage = state.storage.read().await;
    Json(storage.clone())
}

#[tokio::main]
async fn main() {
    // Initialize tracing
    tracing_subscriber::init();

    let app_state = Arc::new(AppState::new());
    
    let app = Router::new()
        .route("/click", post(record_click))
        .route("/stats/:campaign_id", axum::routing::get(get_campaign_stats))
        .route("/stats", axum::routing::get(get_all_stats))
        .with_state(app_state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();
    
    println!("🚀 Ad Click Aggregator running on http://0.0.0.0:3000");
    
    axum::serve(listener, app).await.unwrap();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_record_click() {
        let state = Arc::new(AppState::new());
        let click = ClickEvent {
            campaign_id: "test_campaign".to_string(),
            user_id: Uuid::new_v4().to_string(),
            timestamp: Utc::now(),
            ip_address: "127.0.0.1".to_string(),
            user_agent: "test".to_string(),
        };

        let response = record_click(State(state), Json(click)).await.unwrap();
        assert_eq!(response.0.total_clicks, 1);
        assert_eq!(response.0.unique_users, 1);
    }
}
