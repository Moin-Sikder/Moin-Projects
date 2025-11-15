# Keylogger in Python

**⚠️ LEGAL DISCLAIMER: FOR EDUCATIONAL PURPOSES ONLY**

This project is designed for cybersecurity education and authorized penetration testing. Unauthorized use is illegal and unethical.

# 🎯 Overview

A sophisticated keylogger implementation written in Python with hybrid bash scripting capabilities. Created as part of cybersecurity coursework to demonstrate system monitoring techniques and background process management.

---

# ✨ Features

* **🔒 Stealth Operation** - Runs completely in background with process hiding
* **📝 Comprehensive Logging** - Captures all keystrokes including special keys
* **⚡ Auto-Dependency Install** - Automatically installs required Python libraries
* **🛠️ Process Management** - Easy start/stop/status monitoring via bash scripts
* **📊 Organized Logs** - Structured logging with timestamps and metadata
* **🎯 Educational Focus** - Designed for cybersecurity learning

# 🚀 Installation

**Prerequisites**

* Python 3.8 or higher
* Linux or macOS system
* Bash shell
* pip package manager

## 🔧 Setup Instructions

**For Python**

```bash
# Clone the repository
git clone https://github.com/Moin-Sikder/Moin-Projects/Cybersecurity/keylogger.git
cd keylogger

# Make scripts executable
chmod +x start_keylogger.sh stop_keylogger.sh keylogger.py
```

**For C**

```bash
# Compile Windows version
gcc keylogger.c -o keylogger.exe -luser32 -lgdi32

# Compile Linux version (experimental)
gcc keylogger.c -o keylogger -lX11 -lXtst
```


# 💻 Usage

## For Python

Starting the Keylogger

```bash
./start_keylogger.sh start
```

**Checking Status**

```bash
./start_keylogger.sh status
```

**Stopping the Keylogger**

```bash
./start_keylogger.sh stop
```

**Viewing Logs**

```bash
./start_keylogger.sh logs
```

**Process Verification (as per instructor requirements)**

```bash
ps aux | grep keylogger.py
```

**Log File Format**

```
=== Keylogger Started at 2025-01-15 14:30:25 ===
User: student
Platform: linux
==================================================
[INFO] Keylogger started at 2025-01-15 14:30:25

Hello[ENTER]
This is a test[BACKSPACE]ing example[SHIFT]![ENTER]
Email: user@example.com[TAB]Password123[ENTER]
```

## For C

**Expected Console Output**

```
🔐 Educational Keylogger - Cybersecurity Project
═══════════════════════════════════════════════
🟢 Keylogger started. Press F12 to stop.
📁 Log file: keylog.txt

⌨️ Keylogger is running in background...
🛑 Press F12 to stop gracefully
💡 Keystrokes are being logged to: keylog.txt
```

**Session Header**

```
═══════════════════════════════════════════════════
🟢 KEYLOGGER SESSION STARTED
═══════════════════════════════════════════════════
📅 Date: Thu Dec 12 14:30:45 2024
🆔 Process ID: 1234
💻 Machine: DESKTOP-ABC123
👤 User: JohnDoe
═══════════════════════════════════════════════════
⌨️  KEYSTROKE LOG:
═══════════════════════════════════════════════════
```

**Keystroke Entries**

```
[14:30:46.123] H
[14:30:46.234] e
[14:30:46.345] l
[14:30:46.456] l
[14:30:46.567] o
[14:30:46.678] [SPACE]
[14:30:46.789] [ENTER]
```

**Session Footer**

```
═══════════════════════════════════════════════════
🔴 KEYLOGGER SESSION ENDED
═══════════════════════════════════════════════════
📅 Start Time: Thu Dec 12 14:30:45 2024
📅 End Time: Thu Dec 12 14:35:22 2024
⏱️  Duration: 04:37
🔢 Total Keystrokes: 247
📊 Average KPM: 53.42
═══════════════════════════════════════════════════
```

# 📁 Project Structure

```
python-keylogger/
│
├── keylogger.c
├── keylogger.py              # Main Python keylogger script
├── readme.md                 # Project documentation
├── start_keylogger.sh        # Bash management script
├── stop_keylogger.sh         # Quick stop script
```

# 🎓 Educational Value

This project demonstrates important cybersecurity concepts:

* **System Programming** - Background process management and daemon operations
* **Input Monitoring** - Low-level keyboard event capturing techniques
* **Stealth Techniques** - Process hiding and system persistence methods
* **Logging Systems** - Structured data collection and storage
* **Bash Scripting** - System automation and process management
* **Ethical Considerations** - Responsible development of security tools

# ⚠️ Warning

**CRITICAL: LEGAL AND ETHICAL USAGE ONLY**

This tool is intended solely for:

* Educational purposes in controlled environments
* Authorized penetration testing with explicit permission
* Cybersecurity research and learning

**PROHIBITED USES:**

* Monitoring systems without explicit authorization
* Illegal surveillance activities
* Academic dishonesty
* Any malicious purposes

**Unauthorized use may violate:**

* Computer fraud and abuse laws
* Privacy regulations
* Academic integrity policies
* Institutional security policies

**REMEMBER: With Great Power Comes Great Responsibility**

---

# 📜 License

This project is licensed under the MIT License. See LICENSE file for details.
