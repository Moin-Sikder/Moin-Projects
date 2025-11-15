package models

import "time"

type ClickEvent struct {
    CampaignID  string    `json:"campaign_id"`
    UserID      string    `json:"user_id"`
    Timestamp   time.Time `json:"timestamp"`
    Source      string    `json:"source"`
    AdID        string    `json:"ad_id"`
}

type ConversionEvent struct {
    CampaignID  string    `json:"campaign_id"`
    UserID      string    `json:"user_id"`
    Timestamp   time.Time `json:"timestamp"`
    Amount      float64   `json:"amount"`
    Product     string    `json:"product"`
}

type CampaignStats struct {
    CampaignID         string    `json:"campaign_id"`
    TotalClicks        int       `json:"total_clicks"`
    TotalConversions   int       `json:"total_conversions"`
    TotalRevenue       float64   `json:"total_revenue"`
    ConversionRate     float64   `json:"conversion_rate"`
    LastUpdated        time.Time `json:"last_updated"`
    UniqueUsers        map[string]bool `json:"-"`
}
