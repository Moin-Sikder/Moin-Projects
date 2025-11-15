# 🚀 Ad Click Aggregator

A high-performance ad click aggregation service built in Rust. This service tracks and analyzes clickstream data for advertising campaigns, providing real-time analytics on total clicks, unique users, and click rates.

## Features

- 📊 Real-time click tracking and aggregation
- 👥 Unique user counting
- ⚡ High-performance concurrent processing
- 📈 Click rate calculations (clicks per second)
- 🔍 Campaign-specific statistics
- 🚀 Built with async/await and thread-safe data structures

## Tech Stack

- **Rust** - Systems programming language
- **Tokio** - Async runtime
- **Axum** - Web framework
- **Serde** - Serialization/deserialization
- **Chrono** - Date and time handling

## API Endpoints

### Record a Click
```bash
POST /click
Content-Type: application/json

{
  "campaign_id": "campaign_123",
  "user_id": "user_456",
  "timestamp": "2023-10-01T12:00:00Z",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0..."
}
