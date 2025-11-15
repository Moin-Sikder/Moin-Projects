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

## How to Run

**Prerequisites**

· Rust Installation: You need to have Rust installed on your system. If you don't have it yet:

```bash
# Install Rust using rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Restart your terminal or run:
source $HOME/.cargo/env

# Verify installation
rustc --version
```

**Step 1: Installation & Running**

```bash
# Build the project (this will download dependencies)
cargo build

# Run the service
cargo run
```

**Step 2: Verify it's Working**

Once running, you should see:

```
🚀 Ad Click Aggregator running on http://0.0.0.0:3000
```

The service is now active and ready to receive requests!

**Testing**

Run the included tests to verify everything works:

```bash
# Run tests
cargo test

# Run with detailed output
cargo test -- --nocapture
```

**Building for Production**

```bash
# Build optimized release version
cargo build --release

# The binary will be at ./target/release/ad-click-aggregator

# Run the production binary
./target/release/ad-click-aggregator
```

## Troubleshooting

* **"command not found: cargo"**: Rust is not installed or not in PATH
* **"Address already in use"**: Change the port in main.rs (line 95)
* **Build errors**: Try cargo clean && cargo build to rebuild dependencies
