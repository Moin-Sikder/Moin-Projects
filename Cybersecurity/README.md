# Keylogger in Python

**⚠️ LEGAL DISCLAIMER: FOR EDUCATIONAL PURPOSES ONLY**

This project is designed for cybersecurity education and authorized penetration testing. Unauthorized use is illegal and unethical.

# 🎯 Overview

A sophisticated keylogger implementation written in Python with hybrid bash scripting capabilities. Created as part of cybersecurity coursework to demonstrate system monitoring techniques and background process management.

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

**Setup Instructions**

```bash
# Clone the repository
git clone https://github.com/Moin-Sikder/Moin-Projects/Cybersecurity/keylogger.git
cd keylogger

# Make scripts executable
chmod +x start_keylogger.sh stop_keylogger.sh keylogger.py
```

# 💻 Usage

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

# 📁 Project Structure

```
python-keylogger/
│
├── keylogger.py              # Main Python keylogger script
├── start_keylogger.sh        # Bash management script
├── stop_keylogger.sh         # Quick stop script
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

# 🔧 Technical Details

**Key Components**

1. keylogger.py - Main Python script featuring:
   · Automatic dependency installation
   · Keyboard event monitoring
   · Log file management
   · Background process handling
2. start_keylogger.sh - Bash management script providing:
   · Process control (start/stop/status)
   · Log management
   · System compatibility checks
3. stop_keylogger.sh - Quick termination script

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
