
# 🚀 VANSH Telegram Auto Bot

<div align="center">

![Version](https://img.shields.io/badge/version-6.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Telegram](https://img.shields.io/badge/telegram-bot-blue.svg)

**A professional, feature-rich Telegram automation bot for broadcasting, auto-replies, and reactions**

[Features](#-features) • [Installation](#-installation) • [Configuration](#-configuration) • [Usage](#-usage) • [Support](#-support)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Advanced Settings](#-advanced-settings)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## 🌟 Overview

VANSH Telegram Auto Bot is a powerful automation tool designed to help you manage your Telegram account efficiently. Whether you need to broadcast messages to multiple groups, auto-reply to private messages, or react to mentions automatically, this bot has you covered.

Built with Python and Telethon, it offers a clean, professional interface with extensive customization options.

---

## ✨ Features

### 🎯 Core Features

- **📢 Auto Broadcasting**
  - Broadcast saved messages to all joined groups
  - Configurable delays between messages (3-8 seconds default)
  - Smart cycle wait time (4 minutes default)
  - Skip already sent messages

- **💬 Auto Reply to DMs**
  - Automatically reply to private messages
  - Configurable cooldown period (2 minutes default)
  - Uses your saved messages as replies
  - Typing indicator support

- **⚡ Auto Reactions**
  - React to group mentions automatically
  - React to personal messages in groups
  - Auto-react to DMs
  - Customizable reaction emojis

- **🎨 DM Only Mode**
  - Focus exclusively on direct messages
  - Pause group broadcasting
  - Perfect for personal account management

### ⚙️ Advanced Features

- **🔧 Fully Configurable Delays**
  - Broadcast delay (min/max)
  - Private reply delay (min/max)
  - Group reaction delay (min/max)
  - DM reaction delay (min/max)
  - Mention reaction delay (min/max)
  - Typing indicator delay (min/max)

- **📊 Statistics Tracking**
  - Messages sent/received
  - Reactions sent
  - DM replies count
  - Broadcasts completed
  - Error tracking
  - Uptime monitoring

- **🛡️ Error Handling**
  - Flood wait detection and handling
  - Automatic error recovery
  - Blacklist management
  - Smart retry mechanism

- **🎨 Professional UI**
  - Clean ASCII art banner
  - Color-coded output
  - Status bars
  - Real-time logging
  - Interactive menus

---

## 📦 Requirements

- Python 3.8 or higher
- Telegram API credentials (API ID and API Hash)
- Active Telegram account
- Internet connection

---

## 🚀 Installation

### Method 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/vanshcz/bulkforward.git

# Navigate to directory
cd bulkforward

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
Method 2: Direct Download
Download the repository as ZIP
Extract to desired location
Open terminal/command prompt in the folder
Run:
Bash

pip install -r requirements.txt
python bot.py
🎯 Quick Start
Step 1: Get Telegram API Credentials
Visit https://my.telegram.org
Log in with your phone number
Go to "API Development Tools"
Create a new application
Copy your API ID and API Hash
Step 2: First Run
Bash

python bot.py
Step 3: Setup
Enter your API ID
Enter your API Hash
Enter your phone number (with country code, e.g., +1234567890)
Enter the verification code sent to your Telegram
If you have 2FA enabled, enter your password
Step 4: Start Using
Navigate through the menu using numbers
Press 1 to start the bot
Press Ctrl+C to stop the bot
⚙️ Configuration
Main Menu Options
text

1. 🚀 Start Bot                    - Start all automation features
2. ⏱️  Configure Delays             - Set custom timing for actions
3. 🔄 Refresh Groups               - Update list of joined groups
4. 📊 View Statistics              - See bot performance stats
5. ⚙️  Toggle Features              - Enable/disable specific features
6. 💬 DM Only Mode                 - Toggle DM-only operation
7. ⏰ Cycle Wait Time              - Set broadcast cycle interval
8. 🎨 Reaction Settings            - Customize reaction emojis
9. 📝 View Logs                    - Check recent activity logs
0. 🚪 Exit                         - Close the application
Default Settings
Setting	Default Value	Description
Broadcast Delay	3-8 seconds	Random delay between broadcasts
Private Reply Delay	2-5 seconds	Random delay before replying
Reply Cooldown	120 seconds	Time between replies to same user
Cycle Wait Time	240 seconds	Wait time after completing broadcast cycle
Broadcast Check	20 seconds	How often to check for new messages
Group Sync	300 seconds	How often to refresh group list
📖 Usage Guide
Broadcasting Messages
Save a message in your "Saved Messages" on Telegram
Start the bot (option 1)
The bot will automatically forward this message to all groups
After completing all groups, it waits for the cycle time
Then checks for new saved messages and repeats
Auto-Reply to DMs
Save a message in your "Saved Messages" (this will be your reply)
Enable "Private Reply" feature (option 5 → option 2)
When someone sends you a DM, the bot auto-replies with your saved message
Cooldown prevents spam (default: 2 minutes per user)
DM Only Mode
Perfect for when you only want to handle direct messages:

Press 6 in the main menu
DM Only Mode is now active
Group broadcasting is paused
DM replies and reactions continue working
Press 6 again to return to full mode
Configuring Delays
Select option 2 from main menu
Choose which delay to configure:
Broadcast Delay: Time between group broadcasts
Private Reply Delay: Time before replying to DMs
Reaction Delays: Time before reacting to messages
Enter minimum and maximum values in seconds
Bot will use random delays within this range
Setting Cycle Wait Time
Select option 7 from main menu
Choose from presets or enter custom time:
1 minute (60s)
2 minutes (120s)
4 minutes (240s) - Default
5 minutes (300s)
10 minutes (600s)
Custom (any number of seconds)
Customizing Reactions
Select option 8 from main menu
Configure reactions for:
Group Reactions: When mentioned in groups
DM Reactions: When receiving DMs
Mention Reactions: When someone replies to your message
Enter emojis separated by spaces
Example: 👍 ❤️ 🔥 😂 😍
🔧 Advanced Settings
Feature Toggles
Enable or disable specific features (option 5):

✅ Group Broadcast - Auto-forward saved messages to groups
✅ Private Reply - Auto-reply to private messages
✅ Group Reactions - React to group mentions
✅ DM Reactions - React to direct messages
✅ Mention Reactions - React when mentioned
⚙️ Typing Indicator - Show "typing..." before replying
🔇 Silent Mode - Reduce console output
🐛 Debug Mode - Show detailed logs
File Structure
text

bulkforward/
│
├── bot.py                  # Main bot script
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── Credentials.txt        # Your API credentials (auto-created)
├── Groups.txt            # List of synced groups (auto-created)
├── Settings.json         # Bot configuration (auto-created)
├── Stats.json           # Statistics data (auto-created)
├── Blacklist.txt        # Blacklisted users/groups (auto-created)
├── bot.log              # Activity log (auto-created)
│
└── sessions/            # Telegram session files (auto-created)
    └── session_*.session
Configuration Files
Settings.json - Contains all bot settings

JSON

{
  "delays": {
    "min_broadcast_delay": 3.0,
    "max_broadcast_delay": 8.0,
    ...
  },
  "intervals": {
    "cycle_wait_time": 240,
    ...
  },
  "features": {
    "enable_group_broadcast": true,
    "dm_only_mode": false,
    ...
  }
}
Blacklist.txt - Format

text

# Blacklist file
# Format: type:id
user:123456789
group:-1001234567890
🛠️ Troubleshooting
Common Issues
Bot doesn't start
Problem: Error when starting the bot

Solutions:

Ensure Python 3.8+ is installed: python --version
Reinstall dependencies: pip install -r requirements.txt --upgrade
Check your API credentials are correct
Verify your phone number format includes country code
Flood wait errors
Problem: "FloodWait: waiting X seconds"

Solutions:

This is normal Telegram rate limiting
The bot handles this automatically
Increase delays in configuration
Reduce broadcast frequency
Not receiving messages in groups
Problem: Bot doesn't forward to all groups

Solutions:

Check if you have admin rights in groups
Refresh group list (option 3)
Some groups may have restrictions
Check blacklist.txt for banned groups
Auto-reply not working
Problem: Bot doesn't reply to DMs

Solutions:

Ensure "Private Reply" is enabled (option 5)
Check if you have a message saved in "Saved Messages"
Verify cooldown period hasn't passed
Check if user is blacklisted
Error Messages
Error	Meaning	Solution
ChatWriteForbiddenError	No permission to write	Check admin status
UserBannedInChannelError	Banned from group	Group is auto-blacklisted
FloodWaitError	Rate limit hit	Wait and bot will retry
PhoneCodeInvalidError	Wrong verification code	Re-enter correct code
🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the repository
Create a feature branch
Bash

git checkout -b feature/AmazingFeature
Commit your changes
Bash

git commit -m 'Add some AmazingFeature'
Push to the branch
Bash

git push origin feature/AmazingFeature
Open a Pull Request
Development Guidelines
Follow PEP 8 style guide
Add comments for complex logic
Test thoroughly before submitting
Update documentation if needed
📄 License
This project is licensed under the MIT License - see below for details:

text

MIT License

Copyright (c) 2024 VANSH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
⚠️ Disclaimer
This bot is for educational and personal use only
Use responsibly and respect Telegram's Terms of Service
Avoid spamming or abusing the automation features
The developers are not responsible for any misuse
Always comply with local laws and regulations
💬 Support
Get Help
Issues: GitHub Issues
Telegram: @skullmodders
Discussions: GitHub Discussions
Frequently Asked Questions
Q: Is this bot safe to use?
A: Yes, it uses official Telegram API through Telethon library.

Q: Can I use this on multiple accounts?
A: Yes, just run multiple instances with different credentials.

Q: Will this get my account banned?
A: If used responsibly with proper delays, no. Avoid spamming.

Q: Can I customize the messages?
A: Yes, simply change your saved message in Telegram.

Q: Does this work on channels?
A: Currently optimized for groups and supergroups.

🎉 Acknowledgments
Telethon - Telegram client library
Colorama - Terminal colors
All contributors and users
📊 Statistics
GitHub stars
GitHub forks
GitHub issues
GitHub pull requests

<div align="center">
Made with ❤️ by VANSH

⭐ Star this repo if you find it useful!

Report Bug • Request Feature • Join Community

</div> ```
