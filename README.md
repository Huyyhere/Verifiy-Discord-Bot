# 🔐 Discord Verification Bot - Complete Setup Guide

## 📋 Table of Contents
- [✨ Features](#-features)
- [🛠 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🤖 Commands](#-commands)
- [🚀 Quick Start](#-quick-start)
- [🔧 Troubleshooting](#-troubleshooting)

---

## ✨ Features

### 🌟 Core Features
- **100% Slash Commands** - Modern Discord interaction system
- **Dual Language Support** - English & Vietnamese (automatic detection)
- **Advanced Verification System** - Quick verify & Captcha verification
- **Smart DM System** - Only sends success notifications when verified
- **Persistent Buttons** - Work even after bot restarts
- **Anti-Spam Protection** - Cooldown system prevents abuse
- **Role Restoration** - Automatically restores roles for returning verified users

### 📊 Analytics & Management
- **Detailed Statistics** - Daily, weekly, monthly, and all-time stats
- **Language Analytics** - Track user language preferences
- **Method Tracking** - Monitor verification method usage
- **Data Export** - Export verification data as JSON/CSV
- **Comprehensive Logging** - Complete audit trail

### 🛡️ Security Features
- **Cooldown Protection** - Prevents spam attempts
- **Math Captcha** - Additional security verification
- **Permission Validation** - Admin commands properly secured
- **Data Backups** - Automatic backup system

---

## 🛠 Installation

### Step 1: Prerequisites
```bash
# Python 3.8+ required
python --version

# Install dependencies
pip install discord.py
```

### Step 2: Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application → Bot
3. Copy Bot Token
4. Enable Privileged Gateway Intents:
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT

### Step 3: Bot Permissions
Required permissions (Permission Integer: `2148100160`):
- ✅ Manage Roles
- ✅ Send Messages  
- ✅ Use Slash Commands
- ✅ Manage Messages
- ✅ Read Message History
- ✅ Embed Links

### Step 4: Invite Bot
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=2148100160&scope=bot%20applications.commands
```

---

## ⚙️ Configuration

### config.json Setup
```json
{
  "TOKEN": "YOUR_BOT_TOKEN_HERE",
  "DEFAULT_SERVER_NAME": "Your Server Name",
  
  "CHANNELS": {
    "verify": 123456789012345678,
    "log": 123456789012345679
  },
  
  "ROLES": {
    "verify": 123456789012345680,
    "member": 123456789012345681,
    "unverified": 123456789012345682
  },
  
  "LINKS": {
    "verify_image": "https://your-image-url.com/verify.png",
    "server_icon": "https://your-server-icon.com/icon.png"
  },
  
  "SETTINGS": {
    "verification_cooldown": 30,
    "enable_captcha": true,
    "auto_role_restoration": true,
    "log_verifications": true,
    "enable_dm_notifications": true
  }
}
```

### Getting Discord IDs
1. Enable Developer Mode in Discord
2. Right-click → Copy ID on:
   - Channels (verify, log)
   - Roles (verify, member, unverified)

### Required Server Setup
**Roles to Create:**
- `Verified` - Given to verified users
- `Member` - Additional member role  
- `Unverified` - New users (optional)

**Channels to Create:**
- `#verify` - Verification channel
- `#logs` - Bot activity logs (optional)

---

## 🤖 Commands

### 👥 User Commands

#### `/verify`
**Description**: Verify your account to access all channels  
**Usage**: `/verify`  
**Cooldown**: 30 seconds (configurable)

#### `/language`
**Description**: Change your language preference  
**Usage**: `/language en` or `/language vi`  
**Options**:
- 🇺🇸 `en` - English
- 🇻🇳 `vi` - Tiếng Việt

### 👑 Admin Commands

#### `/setup`
**Description**: Setup verification system in current server  
**Usage**: `/setup`  
**Permission**: Administrator  
**Function**: Creates verification message with buttons

#### `/stats [period]`
**Description**: View detailed verification statistics  
**Usage**: `/stats today`, `/stats week`, `/stats month`, `/stats all`  
**Permission**: Manage Server  
**Shows**: Verifications count, methods used, language distribution

#### `/userinfo [user]`
**Description**: Get detailed user verification information  
**Usage**: `/userinfo @user` or `/userinfo`  
**Permission**: Manage Server  
**Shows**: Verification status, method used, timestamps

#### `/reload`
**Description**: Reload bot configuration without restart  
**Usage**: `/reload`  
**Permission**: Administrator  
**Function**: Reloads config.json changes

#### `/export [format]`
**Description**: Export verification data  
**Usage**: `/export json` or `/export csv`  
**Permission**: Administrator  
**Output**: Downloads data file with all verification records

---

## 🚀 Quick Start

### 1. Download & Setup
```bash
# Create project folder
mkdir discord-verification-bot
cd discord-verification-bot

# Download bot files
# bot.py, config.json

# Install dependencies
pip install discord.py
```

### 2. Configure Bot
```json
{
  "TOKEN": "YOUR_ACTUAL_BOT_TOKEN",
  "DEFAULT_SERVER_NAME": "My Discord Server",
  "CHANNELS": {
    "verify": 1234567890123456789,
    "log": 1234567890123456790
  },
  "ROLES": {
    "verify": 1234567890123456791,
    "member": 1234567890123456792,
    "unverified": 1234567890123456793
  }
}
```

### 3. Run Bot
```bash
python bot.py
```

### 4. Setup Verification
1. Run `/setup` in your Discord server
2. Bot creates verification message in #verify channel
3. Users can now click buttons to verify
4. Test the system yourself!

---

## 🔄 Verification Flow

### New User Journey
1. **User Joins** → Gets "Unverified" role (if configured)
2. **Goes to #verify** → Sees verification message with buttons
3. **Chooses Method**:
   - ✅ **Quick Verify** - Instant (1-click)
   - 🔐 **Captcha Verify** - Solve math problem
4. **Success** → Gets roles + welcome DM
5. **Full Access** → Can use all channels

### Returning User
- Bot automatically detects previously verified users
- Restores verification status immediately
- No need to verify again

---

## 📊 Analytics Dashboard

### Available Statistics
- **Daily**: Today's verification count
- **Weekly**: Past 7 days verification count  
- **Monthly**: Past 30 days verification count
- **All Time**: Total verifications since setup

### Method Tracking
- Quick Verify usage
- Captcha Verify usage
- Slash command usage

### Language Distribution  
- English users count
- Vietnamese users count
- User language preferences

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ "Bot Not Responding"
**Causes:**
- Bot offline
- Missing permissions
- Invalid token

**Solutions:**
- Check bot status in Discord
- Verify bot permissions
- Confirm token in config.json
- Check console logs

#### ❌ "Buttons Not Working"
**Causes:**
- Bot restarted recently
- Permission issues
- Channel misconfiguration

**Solutions:**
- Run `/setup` again
- Check "Use Slash Commands" permission
- Verify channel IDs in config

#### ❌ "Roles Not Assigned"
**Causes:**
- Bot role hierarchy too low
- Missing "Manage Roles" permission
- Invalid role IDs

**Solutions:**
- Move bot role above assigned roles
- Check role permissions
- Verify role IDs in config.json

#### ❌ "No DM Received"
**Causes:**
- User has DMs disabled
- Bot lacks DM permissions

**Solutions:**
- This is normal Discord behavior
- Users must enable DMs from server members
- Bot logs will show "DMs disabled"

### Error Messages Guide
- `Missing Permissions` → Check bot permissions
- `Role Not Found` → Verify role IDs in config
- `Channel Not Found` → Verify channel IDs in config
- `Invalid Token` → Check bot token in config

---

## 🎨 Customization

### Language System
- Easy to add new languages
- Per-user language preferences
- Automatic language detection
- Fallback to English

### Message Customization
Edit language dictionaries in bot.py:
```python
"verification_successful": "🎉 Your custom success message!",
"welcome_title": "🔐 Welcome to {server_name}",
```

### Visual Customization
- Custom verification images
- Server-specific branding
- Configurable embed colors
- Custom footer messages

### Advanced Settings
```json
"SETTINGS": {
  "verification_cooldown": 30,        // Cooldown in seconds
  "enable_captcha": true,             // Enable captcha option
  "auto_role_restoration": true,      // Auto-restore roles
  "log_verifications": true,          // Log to channel
  "enable_dm_notifications": true,    // Send success DMs
  "max_verification_attempts": 3,     // Max attempts per user
  "verification_timeout": 300         // Modal timeout
}
```

---

## 📝 File Structure

```
discord-verification-bot/
├── bot.py                 # Main bot file
├── config.json           # Configuration
├── bot.log              # Bot logs
├── data/                # Data storage
│   ├── verified_users.json
│   ├── user_languages.json
│   └── analytics.json
└── README.md           # This guide
```

---

## 🔐 Security Best Practices

### Bot Token Security
- ❌ Never share your bot token
- ❌ Don't commit token to public repositories
- ✅ Use environment variables in production
- ✅ Regenerate token if compromised

### Permission Management
- ✅ Give bot minimum required permissions
- ✅ Regularly audit bot permissions
- ✅ Use role hierarchy properly
- ✅ Monitor bot activity logs

### Data Protection
- ✅ Regular data backups (automatic)
- ✅ Secure file permissions
- ✅ Monitor unusual activity
- ✅ Keep logs for troubleshooting

---

## ❓ FAQ

**Q: Can I use this on multiple servers?**  
A: Yes, but each server needs separate role/channel IDs in config.

**Q: How do I backup my data?**  
A: Bot auto-backups data. Manual backup: copy `data/` folder.

**Q: Can I modify verification requirements?**  
A: Yes, edit the `verify_user()` method in bot.py.

**Q: What if someone loses verification?**  
A: Run `/userinfo @user` to check status, manually assign roles if needed.

**Q: How do I add more languages?**  
A: Edit the `LanguageManager` class in bot.py with new language dictionary.

**Q: Can I customize the verification message?**  
A: Yes, edit the language dictionaries and re-run `/setup`.

---

## 🚀 Quick Commands Reference

| Command | Purpose | Permission |
|---------|---------|------------|
| `/verify` | Verify account | Everyone |
| `/language` | Change language | Everyone |
| `/setup` | Setup verification | Admin |
| `/stats` | View statistics | Manage Server |
| `/userinfo` | User details | Manage Server |
| `/reload` | Reload config | Admin |
| `/export` | Export data | Admin |

---

## 🎯 Pro Tips

### For Server Owners
- Set clear verification channel permissions
- Use verification channel for announcements
- Monitor verification statistics regularly
- Keep bot logs for troubleshooting

### For Users
- Enable DMs to receive success notifications
- Use `/language` to set preferred language
- Contact admins if verification fails
- Check cooldown timer before retrying

### For Developers
- Check logs for error details
- Test changes in development server
- Backup data before major updates
- Monitor bot performance metrics

---

## 📞 Support

### Getting Help
1. Check this documentation first
2. Review bot logs for errors
3. Verify Discord permissions
4. Test in a development server

### Reporting Issues
Include in your report:
- Error messages from logs
- Bot configuration (hide token)
- Steps to reproduce issue
- Discord server setup details

---

**🎉 Congratulations! Your Discord Verification Bot is now ready to secure your server!**
