#!/bin/bash

# crypto_sim.sh - Educational Ransomware Simulation
# WARNING: FOR EDUCATIONAL PURPOSES ONLY!
# This script demonstrates how ransomware works in a controlled sandbox environment.

SANDBOX_DIR="./crypto_sandbox"
KEY_FILE="decryption_key.txt"
LOG_FILE="ransom_note.txt"
VERSION="1.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    cat << "EOF"
    
  ____                  _                  _   _           _       
 / ___|_ __ _   _ _ __ | |_ ___   ___ ___ | | | | __ _ ___| |_ ___ 
| |   | '__| | | | '_ \| __/ _ \ / __/ _ \| |_| |/ _` / __| __/ _ \
| |___| |  | |_| | |_) | || (_) | (_| (_) |  _  | (_| \__ \ ||  __/
 \____|_|   \__, | .__/ \__\___/ \___\___/|_| |_|\__,_|___/\__\___|
            |___/|_|                                               
            Educational Ransomware Simulator v1.0
            FOR LEARNING PURPOSES ONLY!

EOF
}

show_warning() {
    echo -e "${RED}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                         WARNING!                               ║"
    echo "║    THIS IS AN EDUCATIONAL TOOL ONLY!                          ║"
    echo "║    Do not use on real files or systems!                        ║"
    echo "║    Created for cybersecurity education and awareness.         ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    sleep 2
}

check_dependencies() {
    local deps=("openssl")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            echo -e "${RED}Error: $dep is not installed. Please install it first.${NC}"
            exit 1
        fi
    done
}

setup_sandbox() {
    echo -e "${BLUE}[+] Setting up educational sandbox...${NC}"
    
    # Create sandbox directory
    mkdir -p "$SANDBOX_DIR"
    
    # Create sample files with different types
    echo "This is a confidential document containing important business data." > "$SANDBOX_DIR/document.pdf"
    echo "Financial records for Q4 2024: Revenue $1,234,567" > "$SANDBOX_DIR/finance.xlsx"
    echo "Database connection string: server=localhost;user=admin;password=TempPass123" > "$SANDBOX_DIR/config.ini"
    echo "Project source code - very valuable intellectual property!" > "$SANDBOX_DIR/source_code.py"
    echo "Personal photos and memories from vacation." > "$SANDBOX_DIR/photos.jpg"
    
    # Create some nested directories and files
    mkdir -p "$SANDBOX_DIR/subfolder"
    echo "Backup configuration file" > "$SANDBOX_DIR/subfolder/backup.conf"
    echo "System logs" > "$SANDBOX_DIR/subfolder/logs.txt"
    
    echo -e "${GREEN}[+] Created sandbox with 7 test files in $SANDBOX_DIR/${NC}"
    echo -e "${YELLOW}[!] Sandbox contains simulated important files${NC}"
}

simulate_encryption() {
    echo -e "${YELLOW}[!] SIMULATION: Starting file encryption process...${NC}"
    sleep 2
    
    # Generate encryption key
    echo -e "${BLUE}[+] Generating encryption key...${NC}"
    key=$(openssl rand -hex 32)
    iv=$(openssl rand -hex 16)
    echo "$key:$iv" > "$KEY_FILE"
    
    # Count files to encrypt
    file_count=0
    while IFS= read -r -d '' file; do
        ((file_count++))
    done < <(find "$SANDBOX_DIR" -type f -print0)
    
    echo -e "${BLUE}[+] Found $file_count files to encrypt${NC}"
    
    # Encrypt each file
    encrypted_count=0
    while IFS= read -r -d '' file; do
        if [[ -f "$file" ]]; then
            echo -e "${YELLOW}[!] Encrypting: $file${NC}"
            
            # Encrypt the file
            if openssl enc -aes-256-cbc -salt -in "$file" -out "$file.encrypted" \
               -K "$key" -iv "$iv" 2>/dev/null; then
                rm "$file"
                ((encrypted_count++))
            fi
            
            # Simulate processing time
            sleep 0.5
        fi
    done < <(find "$SANDBOX_DIR" -type f -print0)
    
    # Create ransom note
    create_ransom_note
    
    echo -e "${RED}[!] ENCRYPTION COMPLETE: $encrypted_count files encrypted${NC}"
    echo -e "${RED}[!] Decryption key saved to: $KEY_FILE${NC}"
    echo -e "${RED}[!] Ransom note created: $LOG_FILE${NC}"
}

create_ransom_note() {
    cat > "$LOG_FILE" << "EOF"

╔════════════════════════════════════════════════════════════════╗
║                      *** WARNING ***                          ║
║                    YOUR FILES ARE ENCRYPTED!                  ║
║                                                                ║
║ All of your important files have been encrypted with military ║
║ grade AES-256 encryption. The files are now inaccessible.     ║
║                                                                ║
║ To decrypt your files and restore access, you need to:        ║
║ 1. Use the decryption key that was generated                  ║
║ 2. Run the decryption command                                 ║
║                                                                ║
║ This is an educational simulation. In real ransomware, you    ║
║ would be asked to pay a ransom to get your files back.        ║
║                                                                ║
║ *** NEVER PAY RANSOMS IN REAL ATTACKS ***                     ║
║ Contact cybersecurity professionals instead!                  ║
║                                                                ║
║ To decrypt your files in this simulation:                     ║
║ ./crypto_sim.sh decrypt                                       ║
╚════════════════════════════════════════════════════════════════╝

EOF
}

decrypt_files() {
    echo -e "${GREEN}[+] Starting file decryption process...${NC}"
    
    if [[ ! -f "$KEY_FILE" ]]; then
        echo -e "${RED}[!] Error: No encryption key found!${NC}"
        echo -e "${YELLOW}[!] Look for $KEY_FILE or restore from backup${NC}"
        exit 1
    fi
    
    # Read key and IV
    IFS=':' read -r key iv < "$KEY_FILE"
    
    # Count encrypted files
    encrypted_count=0
    while IFS= read -r -d '' file; do
        if [[ "$file" == *.encrypted ]]; then
            ((encrypted_count++))
        fi
    done < <(find "$SANDBOX_DIR" -type f -name "*.encrypted" -print0)
    
    echo -e "${BLUE}[+] Found $encrypted_count encrypted files${NC}"
    
    # Decrypt each file
    decrypted_count=0
    while IFS= read -r -d '' file; do
        if [[ "$file" == *.encrypted ]]; then
            original_file="${file%.encrypted}"
            echo -e "${GREEN}[+] Decrypting: $file${NC}"
            
            if openssl enc -aes-256-cbc -d -in "$file" -out "$original_file" \
               -K "$key" -iv "$iv" 2>/dev/null; then
                rm "$file"
                ((decrypted_count++))
            else
                echo -e "${RED}[!] Failed to decrypt: $file${NC}"
            fi
        fi
    done < <(find "$SANDBOX_DIR" -type f -name "*.encrypted" -print0)
    
    # Clean up
    rm -f "$KEY_FILE" "$LOG_FILE"
    
    echo -e "${GREEN}[✓] DECRYPTION COMPLETE: $decrypted_count files restored${NC}"
    echo -e "${GREEN}[✓] All files have been successfully decrypted!${NC}"
}

show_status() {
    echo -e "${BLUE}[+] Current System Status:${NC}"
    
    if [[ -f "$KEY_FILE" ]]; then
        echo -e "${RED}[!] FILES ARE ENCRYPTED${NC}"
        encrypted_files=$(find "$SANDBOX_DIR" -name "*.encrypted" | wc -l)
        echo -e "${RED}[!] Encrypted files: $encrypted_files${NC}"
    else
        echo -e "${GREEN}[✓] Files are not encrypted${NC}"
    fi
    
    if [[ -d "$SANDBOX_DIR" ]]; then
        total_files=$(find "$SANDBOX_DIR" -type f | wc -l)
        echo -e "${BLUE}[+] Total files in sandbox: $total_files${NC}"
    fi
}

cleanup() {
    echo -e "${YELLOW}[!] Cleaning up...${NC}"
    rm -rf "$SANDBOX_DIR"
    rm -f "$KEY_FILE" "$LOG_FILE"
    echo -e "${GREEN}[✓] Cleanup complete${NC}"
}

show_help() {
    print_banner
    cat << "EOF"

Usage: ./crypto_sim.sh [command]

Commands:
  setup     - Create educational sandbox with test files
  encrypt   - Simulate ransomware encryption (educational)
  decrypt   - Decrypt files using saved key
  status    - Show current encryption status
  cleanup   - Remove all sandbox files and keys
  help      - Show this help message

Educational Purpose:
This tool demonstrates how ransomware works in a safe, controlled environment.
It shows the importance of:
- Regular backups
- Security awareness
- Encryption principles

WARNING: Only run in test environments!
EOF
}

# Main script execution
main() {
    check_dependencies
    
    case "${1:-help}" in
        "setup")
            show_warning
            setup_sandbox
            ;;
        "encrypt")
            show_warning
            if [[ ! -d "$SANDBOX_DIR" ]]; then
                echo -e "${RED}[!] Sandbox not found. Run './crypto_sim.sh setup' first.${NC}"
                exit 1
            fi
            simulate_encryption
            ;;
        "decrypt")
            decrypt_files
            ;;
        "status")
            show_status
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"