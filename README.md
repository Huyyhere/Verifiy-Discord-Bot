# 🔐 Discord Verification Bot

A verification bot for Discord servers with multi-language support (🇬🇧 English / 🇻🇳 Vietnamese).  
Includes auto-role restoration, DM notifications, simple captcha system, and logging.

---

## 🚀 Features
- ✅ Verify members via **reaction** or **button**.  
- 🔢 Supports **Captcha (math question)** for verification.  
- 📩 Sends DM notification when verification succeeds or when members return.  
- 🔄 Automatically **restores roles** for previously verified members.  
- 🌍 Multi-language support (English, Vietnamese).  
- 📊 Verification logs & basic statistics.  

---

## 📂 Project Structure
```
.
├── config.json          # Bot configuration
├── language-en.json     # English language file
├── language-vi.json     # Vietnamese language file
├── main.py              # Main bot runner
└── utils.py             # Utilities (Config, DataManager, Captcha, Button...)
```

---

## ⚙️ Configuration (`config.json`)
```json
{
  "TOKEN": "YOUR_DISCORD_BOT_TOKEN",
  "SERVER_NAME": "Your Server Name",
  "GUILD_ID": 123456789012345678,
  "CHANNELS": {
    "verify": 123456789012345678,
    "log": 123456789012345678
  },
  "ROLES": {
    "verify": 123456789012345678,
    "unverified": 123456789012345678
  },
  "LINKS": {
    "verify_image": "https://example.com/verify-banner.png",
    "server_icon": "https://example.com/server-icon.png",
    "thumbnail": "None"
  },
  "DATA": {
    "folder": "data",
    "verified_users_file": "data/verified_users.json"
  },
  "SETTINGS": {
    "verification_cooldown": 30,
    "enable_captcha": true,
    "auto_role_restoration": true,
    "default_language": "en",
    "enable_dm_notifications": true,
    "max_verification_attempts": 3,
    "verification_timeout": 300,
    "button_emoji": "✅",
    "verification_type": "button"
  }
}
```

📌 **Notes:**  
- `TOKEN`: replace with your bot token (from [Discord Developer Portal](https://discord.com/developers/applications)).  
- `GUILD_ID`, `CHANNELS`, `ROLES`: use Discord Developer Mode to copy IDs.  
- `verification_type`: `"button"` or `"reaction"`.  

---

## 📦 Installation
Requires Python **3.9+**

```bash
# Clone the repository
git clone https://github.com/Huyyhere/Verifiy-Discord-Bot.git
cd Verifiy-Discord-Bot

# Install dependencies
pip install -U discord.py
```

---

## ▶️ Run the bot
```bash
python main.py
```

---

## 🌍 Language Support
- `language-en.json`: English  
- `language-vi.json`: Vietnamese  

Change the default in `config.json`:
```json
"default_language": "en"
```

---

## 📝 Notes
- Bot automatically creates `data/` folder and `verified_users.json` to store verified users.  
- Logs are stored in `bot.log`.  

---

🔗 GitHub: [Verifiy-Discord-Bot](https://github.com/Huyyhere/Verifiy-Discord-Bot)
