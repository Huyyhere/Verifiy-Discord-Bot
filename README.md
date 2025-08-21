🌟 Discord Verification Bot 🌟
A simple Discord bot for member verification, assigning an "unverified" role to new members and granting a "verified" role upon verification via button or reaction. Supports bilingual messages (English/Vietnamese) and customizable embeds with thumbnails. 🚀
✨ Features

🔐 Verification: Verify via button or reaction, with optional CAPTCHA.
🎭 Role Management: Auto-assigns "unverified" role to new members, grants "verified" role after verification, and restores roles for returning members.
🌍 Bilingual Support: English (language-en.json) and Vietnamese (language-vi.json).
🖼️ Custom Embeds: Supports main image and thumbnail (disable with "None").
💌 DM Notifications: Sends welcome messages on verification or role restoration.
📊 Logging: Logs events to a channel and bot.log, tracks verification stats.

📦 Requirements

🐍 Python: 3.8+ (python.org).
📚 Library: discord.py (pip install discord.py).
🔑 Bot Token: From Discord Developer Portal.
🏠 Discord Server: Bot needs specific permissions (see Bot Permissions).

📂 Project Structure
├── config.json
├── language-en.json
├── language-vi.json
├── features/
│   ├── utils.py
├── main.py
├── bot.log (auto-generated)
├── data/
│   ├── verified_users.json (auto-generated)

🔧 Setup

Install Python: Download 3.8+ from python.org.
Install discord.py:pip install discord.py


Clone Repository: Download or clone this repo to your machine.
Configure: Update config.json and language files (see Configuration).
Invite Bot: Create a bot at Discord Developer Portal, copy the token to config.json, and invite it to your server with required permissions.
Run Bot:python main.py

Check bot.log for startup messages (e.g., "Loaded Vietnamese language file").

⚙️ Configuration
📝 config.json
Edit config.json to match your server:
{
  "TOKEN": "YOUR_BOT_TOKEN",
  "SERVER_NAME": "Your Server",
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
    "verify_image": "https://example.com/image.jpg",
    "server_icon": "https://example.com/icon.png",
    "thumbnail": "None"
  },
  "DATA": {
    "folder": "data",
    "verified_users_file": "data/verified_users.json"
  },
  "SETTINGS": {
    "verification_cooldown": 30,
    "enable_captcha": false,
    "auto_role_restoration": true,
    "default_language": "vi",
    "enable_dm_notifications": true,
    "max_verification_attempts": 3,
    "verification_timeout": 300,
    "button_emoji": "✅",
    "verification_type": "button"
  }
}


🔑 TOKEN: Bot token from Discord Developer Portal.
🏠 SERVER_NAME: Your server’s name (e.g., "PAWII").
🆔 GUILD_ID: Server ID (right-click server > Copy ID).
📢 CHANNELS:
verify: ID of verification channel.
log: ID of logging channel.


🎭 ROLES:
verify: ID of role granted after verification.
unverified: ID of role for new members.


🖼️ LINKS:
verify_image: URL for embed’s main image (optional).
server_icon: URL for server icon in DMs (optional).
thumbnail: URL for verification embed thumbnail, set to "None" to disable.


📁 DATA: Paths for user data (keep default).
⚙️ SETTINGS:
verification_cooldown: Seconds to wait before retrying.
enable_captcha: true for CAPTCHA, false for direct verification.
auto_role_restoration: true to restore roles for returning members.
default_language: "vi" (Vietnamese) or "en" (English).
enable_dm_notifications: true to send DMs.
max_verification_attempts: Max CAPTCHA attempts.
verification_timeout: CAPTCHA timeout (seconds).
button_emoji: Emoji for button/reaction (e.g., "✅", "🔓", or "<:name:id>").
verification_type: "button" or "reaction".



🌐 Language Files

Files: language-en.json (English) and language-vi.json (Vietnamese).
Purpose: Define text for embeds, DMs, and logs.
Editing:
Open language-vi.json or language-en.json in a text editor.
Modify text in keys like welcome_embed.title, verification.successful, etc.
Example (Vietnamese):"welcome_embed": {
  "title": "Chào mừng đến {server_name}",
  "description": "Nhấn nút hoặc phản ứng để xác minh!"
}


Ensure all required keys (welcome_embed, verification, etc.) remain to avoid errors.
Save and restart bot to apply changes.



🤖 Bot Permissions
The bot requires these Discord permissions:

📜 Manage Roles: To assign/remove unverified and verify roles.
💬 Send Messages: To send verification embed and logs.
🔗 Embed Links: For rich embeds.
😊 Add Reactions: For reaction-based verification.
📖 Read Message History: To detect reactions.

Setup: In Discord Developer Portal, generate an invite link with these permissions and add the bot to your server.
💬 Bot Messages
Messages depend on default_language ("vi" or "en"):

Verification Embed (in verify channel):
🇻🇳: "Chào mừng đến {server_name}\nXác minh để truy cập tất cả kênh.\nNhấn nút bên dưới hoặc thêm phản ứng để được xác minh:"
🇬🇧: "Welcome to {server_name}\nVerify to access all channels.\nClick the button below or add a reaction to get verified:"


CAPTCHA (if enabled):
🇻🇳: "Xác Minh Bảo Mật\nGiải bài toán: {num1} + {num2} = ?"
🇬🇧: "Security Verification\nSolve: {num1} + {num2} = ?"


DM Notifications:
Success (🇻🇳): "Xác Minh Thành Công!\nChúc mừng! Bạn đã được xác minh trong {server_name}."
Success (🇬🇧): "Verification Successful!\nYou have been verified in {server_name}."
Welcome Back (🇻🇳): "Chào Mừng Trở Lại!\nTrạng thái xác minh đã được khôi phục."


Logs (in log channel):
🇻🇳: "Người Dùng Đã Xác Minh\nNgười dùng: {user_mention}\nPhương thức: {method}"
🇬🇧: "User Verified\nUser: {user_mention}\nMethod: {method}"


Errors:
🇻🇳: "Bạn đã được xác minh rồi!" or "Vui lòng chờ {seconds} giây."
🇬🇧: "You are already verified!" or "Please wait {seconds} seconds."



📚 How It Works

🔐 Verification:
Button (verification_type: "button"): Shows a button with button_emoji.
Reaction (verification_type: "reaction"): Bot adds button_emoji for users to react.
CAPTCHA (if enabled): Solve a math problem to verify.


🎭 Roles: Assigns unverified to new members, grants verify on verification, restores roles for returning users.
🌍 Language: Uses language-vi.json or language-en.json based on default_language.
📊 Logging: Logs events to bot.log and log channel, tracks verification stats.

🛠️ Troubleshooting

Bot Won’t Start: Check bot.log for errors, ensure config.json has valid TOKEN, IDs.
No Verification Message: Verify verify channel ID and bot permissions (Send Messages, Embed Links).
Language Errors: Ensure language-en.json and language-vi.json exist with all keys.
Thumbnail Missing: Check LINKS.thumbnail for valid URL or set to "None".
Reaction Issues: Ensure bot has Add Reactions permission and button_emoji is valid.

🎨 Customization

🔄 Verification Type: Set verification_type to "button" or "reaction".
🖼️ Embed: Update verify_image, thumbnail in config.json, or edit welcome_embed in language files.
⚙️ Settings: Adjust enable_captcha, default_language, etc. in config.json.


⭐ Star this repo if you find it helpful! For issues, check bot.log or open a GitHub issue. 🎉
