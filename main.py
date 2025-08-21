import discord
import logging
from datetime import datetime, timezone
from utils import Config, DataManager, LanguageManager, Colors, create_verify_view

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log', encoding='utf-8'), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

class VerificationBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.config = Config()
        self.data_manager = DataManager(self.config)
        
        default_lang = self.config.get("SETTINGS", {}).get("default_language", "en")
        self.lang = LanguageManager(default_lang)
        
        if default_lang not in self.lang.languages:
            logger.error(f"Default language '{default_lang}' not loaded! Falling back to 'en'")
            self.lang.default_lang = "en"
        
        self.verification_cooldowns = {}
        self.verification_message_id = None
        self.analytics = {"total_verifications": 0, "daily_stats": {}, "verification_methods": {}}
        self.guild_name = self.config.get("SERVER_NAME")
        self.channels = self.config.get("CHANNELS", {})
        self.roles = self.config.get("ROLES", {})
        self.links = self.config.get("LINKS", {})
        self.settings = self.config.get("SETTINGS", {})
        self.guild = None

    def create_embed(self, description: str, color: int, title: str = None) -> discord.Embed:
        embed = discord.Embed(description=description, color=color, timestamp=datetime.now(timezone.utc))
        if title:
            embed.title = title
        embed.set_footer(text=self.lang.get("welcome_embed.footer", server_name=self.guild_name))
        return embed

    async def on_ready(self):
        logger.info(f"Bot logged in as {self.user}")
        logger.info(f"Connected to {len(self.guilds)} servers")
        
        guild_id = self.config.get("GUILD_ID")
        if guild_id:
            self.guild = self.get_guild(guild_id)
            if self.guild:
                logger.info(f"Found guild: {self.guild.name} (ID: {guild_id})")
            else:
                logger.error(f"Guild with ID {guild_id} not found! Bot may not be in this server.")
                return
        else:
            logger.warning("GUILD_ID not set in config, trying to find from verify channel...")
            verify_channel_id = self.channels.get("verify")
            if verify_channel_id:
                verify_channel = self.get_channel(verify_channel_id)
                if verify_channel:
                    self.guild = verify_channel.guild
                    logger.info(f"Found guild from channel: {self.guild.name}")
                else:
                    logger.error("Verify channel not found!")
            
        if not self.guild:
            logger.error("Could not determine guild. Please set GUILD_ID in config.json")
            return
            
        logger.info("Bot is ready!")
        await self.setup_verification_message()

    async def setup_verification_message(self):
        channel = self.get_channel(self.channels.get("verify"))
        if not channel or not self.guild:
            logger.error("Verify channel or guild not found in config.")
            return
            
        embed = discord.Embed(
            title=self.lang.get("welcome_embed.title", server_name=self.guild_name),
            description=self.lang.get("welcome_embed.description"),
            color=Colors.INFO
        ).add_field(
            name=self.lang.get("welcome_embed.field_title"), 
            value=self.lang.get("welcome_embed.field_content"), 
            inline=False
        )
        
        if self.links.get("verify_image"):
            embed.set_image(url=self.links["verify_image"])
        
        thumbnail = self.links.get("thumbnail")
        if thumbnail and thumbnail.lower() != "none":
            embed.set_thumbnail(url=thumbnail)
        
        verification_type = self.settings.get("verification_type", "button")
        if verification_type == "button":
            message = await channel.send(embed=embed, view=create_verify_view(self))
        elif verification_type == "reaction":
            message = await channel.send(embed=embed)
            emoji = self.config.get("SETTINGS", {}).get("button_emoji", "✅")
            await message.add_reaction(emoji)
        
        self.verification_message_id = message.id
        logger.info(f"Verification message sent with ID: {message.id}")

    async def on_raw_reaction_add(self, payload):
        if self.settings.get("verification_type", "button") != "reaction":
            return
        if payload.message_id != self.verification_message_id:
            return
        if payload.user_id == self.user.id:
            return
            
        guild = self.get_guild(payload.guild_id)
        if not guild:
            return
            
        member = guild.get_member(payload.user_id)
        if not member:
            return
            
        expected_emoji = self.config.get("SETTINGS", {}).get("button_emoji", "✅")
        if str(payload.emoji) == expected_emoji:
            await self.verify_user(member, guild, "reaction", None)

    async def verify_user(self, user, guild, source, interaction=None):
        if not guild:
            return
            
        try:
            verify_role = guild.get_role(self.roles.get("verify"))
            unverified_role = guild.get_role(self.roles.get("unverified"))

            if not verify_role:
                if interaction:
                    await interaction.response.send_message(
                        embed=self.create_embed(self.lang.get("verification.role_not_found"), Colors.ERROR), 
                        ephemeral=True
                    )
                return

            if verify_role in user.roles:
                if interaction:
                    await interaction.response.send_message(
                        embed=self.create_embed(self.lang.get("verification.already_verified"), Colors.INFO), 
                        ephemeral=True
                    )
                return

            cooldown = self.get_cooldown_remaining(user.id)
            if cooldown > 0:
                if interaction:
                    await interaction.response.send_message(
                        embed=self.create_embed(
                            self.lang.get("verification.cooldown_message", seconds=cooldown), 
                            Colors.WARNING
                        ), 
                        ephemeral=True
                    )
                return

            self.verification_cooldowns[user.id] = datetime.now(timezone.utc)
            
            roles_to_add = [verify_role] if verify_role else []
            roles_to_remove = [unverified_role] if unverified_role and unverified_role in user.roles else []

            if roles_to_remove:
                await user.remove_roles(*roles_to_remove, reason=f"Verified via {source}")
                
            if roles_to_add:
                await user.add_roles(*roles_to_add, reason=f"Verified via {source}")

            users = self.data_manager.get_verified_users()
            if not any(u["id"] == user.id for u in users):
                users.append({
                    "id": user.id, 
                    "name": str(user), 
                    "verified_at": str(datetime.now(timezone.utc)), 
                    "method": source
                })
                self.data_manager.save_verified_users(users)
                
                self.analytics["total_verifications"] += 1
                today = str(datetime.now(timezone.utc).date())
                self.analytics["daily_stats"][today] = self.analytics["daily_stats"].get(today, 0) + 1
                self.analytics["verification_methods"][source] = self.analytics["verification_methods"].get(source, 0) + 1

            if self.settings.get("enable_dm_notifications", True):
                try:
                    embed = discord.Embed(
                        title=self.lang.get("dm_notifications.verify_success.title"), 
                        description=self.lang.get("dm_notifications.verify_success.description", server_name=self.guild_name), 
                        color=Colors.SUCCESS
                    )
                    embed.add_field(
                        name=self.lang.get("dm_notifications.verify_success.features_title"), 
                        value=self.lang.get("dm_notifications.verify_success.features_content"), 
                        inline=False
                    )
                    if self.links.get("server_icon"):
                        embed.set_thumbnail(url=self.links["server_icon"])
                    embed.set_footer(text=self.lang.get("dm_notifications.verify_success.footer", server_name=self.guild_name))
                    await user.send(embed=embed)
                except discord.Forbidden:
                    logger.warning(f"Could not send DM to {user}")

            if interaction:
                await interaction.response.send_message(
                    embed=self.create_embed(self.lang.get("verification.successful"), Colors.SUCCESS), 
                    ephemeral=True
                )
            
            log_channel = self.get_channel(self.channels.get("log"))
            if log_channel:
                log_embed = discord.Embed(
                    title=self.lang.get("logging.user_verified.title"),
                    description=self.lang.get("logging.user_verified.description", 
                                            user_mention=user.mention, 
                                            user_name=str(user), 
                                            method=source.title(), 
                                            timestamp=int(datetime.now(timezone.utc).timestamp())),
                    color=Colors.SUCCESS
                )
                await log_channel.send(embed=log_embed)
                
        except discord.Forbidden:
            if interaction:
                await interaction.response.send_message(
                    embed=self.create_embed(self.lang.get("verification.failed"), Colors.ERROR), 
                    ephemeral=True
                )
            logger.error(f"Missing permissions to verify {user}")
        except Exception as e:
            logger.error(f"Error during verification: {e}")
            if interaction and not interaction.response.is_done():
                await interaction.response.send_message(
                    embed=self.create_embed(self.lang.get("verification.failed"), Colors.ERROR), 
                    ephemeral=True
                )

    def get_cooldown_remaining(self, user_id: int) -> int:
        if user_id not in self.verification_cooldowns:
            return 0
        elapsed = (datetime.now(timezone.utc) - self.verification_cooldowns[user_id]).total_seconds()
        return max(0, int(self.settings.get("verification_cooldown", 30) - elapsed))

    async def on_member_join(self, member):
        if member.guild != self.guild:
            return
            
        if self.settings.get("auto_role_restoration", True):
            verified_users = self.data_manager.get_verified_users()
            user_data = next((u for u in verified_users if u["id"] == member.id), None)
            
            if user_data:
                verify_role = member.guild.get_role(self.roles.get("verify"))
                
                roles_to_add = [verify_role] if verify_role else []
                
                if roles_to_add:
                    try:
                        await member.add_roles(*roles_to_add, reason="Auto role restoration - previously verified")
                        logger.info(f"Restored roles for returning verified user: {member}")
                        
                        if self.settings.get("enable_dm_notifications", True):
                            try:
                                embed = discord.Embed(
                                    title=self.lang.get("dm_notifications.welcome_back.title"),
                                    description=self.lang.get("dm_notifications.welcome_back.description", server_name=self.guild_name),
                                    color=Colors.SUCCESS
                                )
                                embed.add_field(
                                    name=self.lang.get("dm_notifications.welcome_back.status_title"),
                                    value=self.lang.get("dm_notifications.welcome_back.status_content"),
                                    inline=False
                                )
                                if self.links.get("server_icon"):
                                    embed.set_thumbnail(url=self.links["server_icon"])
                                embed.set_footer(text=self.lang.get("dm_notifications.welcome_back.footer", server_name=self.guild_name))
                                await member.send(embed=embed)
                            except discord.Forbidden:
                                logger.warning(f"Could not send welcome back DM to {member}")
                        
                        log_channel = self.get_channel(self.channels.get("log"))
                        if log_channel:
                            log_embed = discord.Embed(
                                title=self.lang.get("logging.auto_restoration.title"),
                                description=self.lang.get("logging.auto_restoration.description", 
                                                        user_mention=member.mention, 
                                                        user_name=str(member), 
                                                        previous_timestamp=int(datetime.fromisoformat(user_data['verified_at'].replace('Z', '+00:00')).timestamp()),
                                                        method=user_data.get('method', 'Unknown')),
                                color=Colors.INFO
                            )
                            await log_channel.send(embed=log_embed)
                    except discord.Forbidden:
                        logger.error(f"Missing permissions to restore roles for {member}")
                    except Exception as e:
                        logger.error(f"Error restoring roles for {member}: {e}")
                
                return
        
        unverified_role = member.guild.get_role(self.roles.get("unverified"))
        if unverified_role:
            try:
                await member.add_roles(unverified_role, reason="Auto-assigned on join")
                logger.info(f"Added unverified role to new member: {member}")
            except discord.Forbidden:
                logger.error(f"Missing permissions to add unverified role to {member}")
            except Exception as e:
                logger.error(f"Error adding unverified role to {member}: {e}")

def main():
    bot = VerificationBot()
    token = bot.config.get("TOKEN")
    
    if not token or token == "YOUR_DISCORD_BOT_TOKEN":
        print("Please configure your bot token in config.json")
        print("Get your token from: https://discord.com/developers/applications")
        return
        
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("Invalid bot token! Check config.json")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        print(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()