#!/bin/bash

# Stop Keylogger Script

LOG_DIR="$HOME/.keylogger_logs"
PID_FILE="$LOG_DIR/keylogger.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "Stopping keylogger (PID: $PID)"
    kill $PID
    rm -f "$PID_FILE"
    echo "Keylogger stopped"
else
    echo "No running keylogger found (PID file missing)"
    echo "Trying to find and kill any keylogger processes..."
    pkill -f "keylogger.py" && echo "Keylogger processes terminated" || echo "No keylogger processes found"
fi
