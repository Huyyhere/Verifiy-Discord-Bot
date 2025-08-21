import discord
from discord.ui import Button, View, Modal, TextInput
import json
import os
import logging
import random
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class Colors:
    SUCCESS = 0x00FF00
    ERROR = 0xFF0000
    WARNING = 0xFFFF00
    INFO = 0x0099FF

class LanguageManager:
    def __init__(self, default_lang="en"):
        self.default_lang = default_lang
        self.languages = {}
        self.load_languages()
    
    def load_languages(self):
        try:
            base_dir = os.path.dirname(__file__)
            
            en_path = os.path.join(base_dir, "language-en.json")
            if os.path.exists(en_path):
                with open(en_path, "r", encoding="utf-8") as f:
                    self.languages["en"] = json.load(f)
                    logger.info("Loaded English language file")
                    logger.debug(f"English language data keys: {list(self.languages['en'].keys())}")
            else:
                logger.error(f"English language file not found at: {en_path}")
            
            vi_path = os.path.join(base_dir, "language-vi.json")
            if os.path.exists(vi_path):
                with open(vi_path, "r", encoding="utf-8") as f:
                    self.languages["vi"] = json.load(f)
                    logger.info("Loaded Vietnamese language file")
                    logger.debug(f"Vietnamese language data keys: {list(self.languages['vi'].keys())}")
            else:
                logger.error(f"Vietnamese language file not found at: {vi_path}")
            
            logger.info(f"Available languages: {list(self.languages.keys())}")
            logger.info(f"Default language: {self.default_lang}")
            
            lang_data = self.languages.get(self.default_lang, {})
            if "welcome_embed" not in lang_data or "verification" not in lang_data:
                logger.error(f"Default language '{self.default_lang}' is missing expected keys! Falling back to English if available.")
                    
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in language files: {e}")
        except Exception as e:
            logger.error(f"Error loading language files: {e}")
    
    def get(self, key: str, lang: str = None, **kwargs) -> str:
        if lang is None:
            lang = self.default_lang
            logger.debug(f"Using default language: {lang}")
            
        lang_data = self.languages.get(lang, self.languages.get("en", {}))
        if not lang_data:
            logger.warning(f"No language data available for '{lang}' or 'en', returning key: {key}")
            return key
        
        keys = key.split('.')
        value = lang_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                logger.warning(f"Key '{key}' not found in language '{lang}', returning key as fallback")
                return key
        
        if isinstance(value, dict):
            logger.warning(f"Key '{key}' points to dict, not string")
            return key
            
        if isinstance(value, str):
            try:
                formatted_value = value.format(**kwargs)
                logger.debug(f"Resolved key '{key}' in language '{lang}' to: {formatted_value}")
                return formatted_value
            except KeyError as e:
                logger.warning(f"Missing format key {e} for string: {value}")
                return value
        
        return str(value)

class Config:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = os.path.join(os.path.dirname(__file__), config_path)
        self.data = self.load_config()
    
    def load_config(self) -> dict:
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {self.config_path} not found! Please create a valid config.json file.")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise
    
    def get(self, key: str, default=None):
        return self.data.get(key, default)

class DataManager:
    def __init__(self, config: Config):
        self.config = config
        self.verified_users_file = config.get("DATA", {}).get("verified_users_file", "data/verified_users.json")
        
        data_folder = config.get("DATA", {}).get("folder", "data")
        os.makedirs(data_folder, exist_ok=True)
        
        if not os.path.exists(self.verified_users_file):
            self.save_json(self.verified_users_file, [])

    def load_json(self, file_path: str, default=None):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Could not load {file_path}: {e}")
            return default or []

    def save_json(self, file_path: str, data):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")

    def get_verified_users(self) -> list:
        return self.load_json(self.verified_users_file)

    def save_verified_users(self, users: list):
        self.save_json(self.verified_users_file, users)

class CaptchaModal(Modal):
    def __init__(self, bot, user_id: int):
        super().__init__(title=bot.lang.get("captcha.title"), timeout=300)
        self.bot = bot
        self.user_id = user_id
        self.num1, self.num2 = random.randint(1, 20), random.randint(1, 20)
        self.answer = self.num1 + self.num2
        
        self.captcha_input = TextInput(
            label=bot.lang.get("captcha.question", num1=self.num1, num2=self.num2),
            placeholder=bot.lang.get("captcha.placeholder"),
            min_length=1, 
            max_length=3, 
            required=True
        )
        self.add_item(self.captcha_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_answer = int(self.captcha_input.value.strip())
            if user_answer == self.answer:
                await interaction.response.defer()
                await self.bot.verify_user(interaction.user, interaction.guild, "captcha", interaction)
            else:
                await interaction.response.send_message(
                    embed=self.bot.create_embed(
                        self.bot.lang.get("captcha.incorrect"), 
                        Colors.ERROR
                    ), 
                    ephemeral=True
                )
        except ValueError:
            await interaction.response.send_message(
                embed=self.bot.create_embed(
                    self.bot.lang.get("captcha.invalid"), 
                    Colors.ERROR
                ), 
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error in captcha modal: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    embed=self.bot.create_embed("An error occurred. Please try again.", Colors.ERROR),
                    ephemeral=True
                )

    async def on_timeout(self):
        logger.info(f"Captcha modal timed out for user {self.user_id}")

class VerifyButton(Button):
    def __init__(self, bot):
        emoji = bot.config.get("SETTINGS", {}).get("button_emoji", None)
        super().__init__(
            label=bot.lang.get("verification.button_label"), 
            style=discord.ButtonStyle.success, 
            custom_id="verify_now",
            emoji=emoji
        )
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        try:
            if self.bot.settings.get("enable_captcha", True):
                await interaction.response.send_modal(CaptchaModal(self.bot, interaction.user.id))
            else:
                await interaction.response.defer()
                await self.bot.verify_user(interaction.user, interaction.guild, "button", interaction)
        except Exception as e:
            logger.error(f"Error in verify button callback: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    embed=self.bot.create_embed("An error occurred. Please try again.", Colors.ERROR),
                    ephemeral=True
                )

def create_verify_view(bot):
    view = View(timeout=None)
    view.add_item(VerifyButton(bot))
    return view
