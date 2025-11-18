# 📧 Personalized Banking Email Dispatcher

![AppleScript](https://img.shields.io/badge/AppleScript-Automation-blue)
![macOS](https://img.shields.io/badge/macOS-Required-lightgrey)
![Banking](https://img.shields.io/badge/Industry-Banking-green)

> **Automate personalized client communications at scale** - Because every client deserves individual attention, even when you're managing hundreds.

## 🚀 What Does This Do?

This AppleScript transforms your Numbers spreadsheet into a powerful email marketing machine! It automatically:

- 📊 **Reads client data** from your Numbers spreadsheet
- ✨ **Personalizes each email** with client-specific information
- 📨 **Creates ready-to-send drafts** in your Mail app
- ⚡ **Processes hundreds of clients** in minutes instead of hours
- 🛡️ **Includes safety features** to prevent accidental sending

## 🎯 Perfect For Banking Professionals

| Use Case | Time Saved | Impact |
|----------|------------|--------|
| **Market Updates** | 2-3 hours weekly | Keep clients informed automatically |
| **Portfolio Reviews** | 1-2 hours monthly | Proactive client engagement |
| **Birthday Wishes** | 30 minutes monthly | Personal touch at scale |
| **Regulatory Updates** | 1 hour quarterly | Compliance made easy |

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **macOS** (10.14 or later)
- ✅ **Numbers** app installed
- ✅ **Mail** app configured with your email account
- ✅ **Script Editor** app (comes with macOS)
- ✅ **Numbers spreadsheet** with client data

## 🛠️ Setup Guide

### Step 1: Prepare Your Spreadsheet

Create a Numbers file with this exact structure:

| A | B | C | D |
|---|---||---|
| **Client Name** | **Email** | **Account** | **Notes** |
| John Smith | john@email.com | 4587 | Premium client |
| Sarah Johnson | sarah@email.com | 8921 | Interested in mortgages |
| Mike Chen | mike@email.com | 3365 | Risk-averse investor |

**📝 Pro Tip:** Save your spreadsheet as "Client Communications.numbers" on your Desktop for easy access.

### Step 2: Customize the Script

Open **Script Editor** (press `Cmd + Space` and type "Script Editor") and paste this code:

```applescript
-- CONFIGURATION SECTION - EDIT THESE VALUES
property emailSubject : "Important Market Update and Portfolio Review"
property emailTemplate : "Dear {{Name}},`n`nIn light of recent market developments, we recommend reviewing your portfolio (account ending {{Account}}). Our team has identified opportunities that align with your financial goals.`n`nKey points to discuss:`n• Portfolio performance review`n• Market outlook analysis`n• Strategic adjustments`n`nPlease schedule a 15-minute call at your convenience.`n`nBest regards,`nYour Dedicated Banking Team"

-- DATA RANGE - Adjust if your spreadsheet has more columns
property dataRange : "A2:D100"

-- REST OF THE SCRIPT (from the main code)...
```

## 🎨 Customization Ideas:

· Change emailSubject to match your campaign
· Modify emailTemplate with your bank's branding
· Adjust dataRange if you have more than 100 clients

Step 3: Configure Security Settings

First-time users need to enable AppleScript permissions:

1. Go to System Settings > Privacy & Security > Automation
2. Check Script Editor and Numbers for automation control
3. Grant Accessibility permissions if prompted

## 🚀 How to Run

Method 1: One-Click Execution

1. Open your Numbers spreadsheet
2. Run the script in Script Editor
3. Watch the magic happen! ✨

Method 2: Save as Application

1. In Script Editor: File > Export
2. Format: Application
3. Save as: "Email Dispatcher.app"
4. Double-click to run anytime!

### 📊 Expected Results

After running the script, you'll see:

```
✅ Email dispatch completed:

✓ Successfully processed: 47 clients
✗ Errors encountered: 2

Review the draft emails in Mail before sending.
```

Then check your Mail app: All personalized emails will be waiting as drafts for your final review!

### 🛡️ Safety Features

Feature Protection
Draft Mode All emails created as drafts first
Error Handling Continues processing even if some emails fail
Data Validation Skips incomplete or invalid entries
Rate Limiting Built-in delays prevent system overload

### 🔧 Advanced Customization

Adding More Personalization Fields

Enhance your template with additional fields:

```applescript
-- Add to your template:
"Dear {{Name}},`n`nAs a valued {{ClientType}} client..."

-- In the data processing, add:
set clientType to item 4 of clientRecord
set personalizedBody to my replaceText(personalizedBody, "{{ClientType}}", clientType)
```

Enable Automatic Sending

⚠️ Use with caution - only after thorough testing!

```applescript
-- Change this line:
-- send

-- To this:
send
```

### 🐛 Troubleshooting

Issue Solution
"Application isn't allowed to send Apple events" Grant permissions in System Settings > Privacy & Security > Automation
Emails not creating Check if Mail app is open and configured properly
Some clients skipped Verify all required fields are filled in spreadsheet
Script runs but nothing happens Ensure your spreadsheet is the active Numbers document

### 📈 Real-World Impact

Time Savings Calculation:

```
Manual Process:
47 clients × 3 minutes each = 141 minutes (2.35 hours)

With This Script:
47 clients × 10 seconds each = 8 minutes

Time Saved: 2 hours 27 minutes per campaign! 🎉
```

## 🤝 Contributing

Found a bug? Have an improvement?

1. Fork this repository
2. Create your feature branch
3. Submit a pull request

## 📄 License

***This project is licensed under the MIT License - see the LICENSE.md file for details.***

### ⚠️ Disclaimer

Important: Always ensure compliance with your organization's email policies and data protection regulations (GDPR, CAN-SPAM, etc.). Test thoroughly with small batches before full deployment. The authors are not responsible for any unintended consequences of using this script.

---

### 💡 Pro Tip: Combine this with calendar automation for complete client communication workflow! Check out our other banking automation scripts.

---

Made with ❤️ for banking professionals who value efficiency and personalization

If this saved you time, consider giving it a ⭐ on GitHub!