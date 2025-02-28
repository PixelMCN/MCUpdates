import nextcord
from nextcord.ext import commands
from models.models import ProjectUpdate, UserSettings
from utils.database import Database
from utils.api import ModAPI
from datetime import datetime

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.api = ModAPI()

    @commands.command(name="setup")
    async def setup(self, ctx, channel: nextcord.TextChannel, project_id: str, platform: str, api_key: str = None):
        settings = {
            'channel_id': channel.id,
            'project_id': project_id,
            'platform': platform.lower(),
            'api_key': api_key
        }
        
        if self.db.save_user_settings(ctx.guild.id, settings):
            await ctx.send(f"Setup complete! Updates will be sent to {channel.mention}")
        else:
            await ctx.send("Failed to save settings. Please try again.")

    @commands.command(name="view_settings")
    async def view_settings(self, ctx):
        settings = self.db.get_user_settings(ctx.guild.id)
        if settings:
            embed = nextcord.Embed(title="Current Settings", color=0x00ff00)
            for setting in settings:
                channel = self.bot.get_channel(setting['channel_id'])
                embed.add_field(
                    name=f"Project: {setting['project_id']}",
                    value=f"Channel: {channel.mention if channel else 'Unknown'}\n"
                          f"Platform: {setting['platform']}\n"
                          f"Last Checked: {setting['last_checked']}",
                    inline=False
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No settings found.")

    @commands.command(name="delete_settings")
    async def delete_settings(self, ctx, project_id: str = None):
        if self.db.delete_user_settings(ctx.guild.id, project_id):
            await ctx.send("Settings deleted successfully.")
        else:
            await ctx.send("Failed to delete settings.")

    @commands.command(name="check_updates")
    async def check_updates(self, ctx, project_id: str = None):
        settings_list = self.db.get_user_settings(ctx.guild.id)
        if not settings_list:
            await ctx.send("No projects configured for updates.")
            return

        for setting_data in settings_list:
            if project_id and setting_data['project_id'] != project_id:
                continue
                
            settings = UserSettings(
                guild_id=ctx.guild.id,
                channel_id=setting_data['channel_id'],
                project_id=setting_data['project_id'],
                platform=setting_data['platform']
            )

            if settings.should_check_updates():
                updates = await self.api.fetch_updates(settings.project_id, settings.platform)
                if updates:
                    # Convert API response to ProjectUpdate object
                    latest = updates[0] if settings.platform == "modrinth" else updates['data'][0]
                    update = ProjectUpdate(
                        title=latest.get("name", "Unknown"),
                        version=latest.get("version_number", latest.get("fileName", "Unknown")),
                        description=latest.get("changelog", "No changelog provided"),
                        url=latest.get("downloadUrl", ""),
                        platform=settings.platform,
                        release_type=latest.get("version_type", latest.get("releaseType", "release")),
                        game_versions=latest.get("gameVersions", []),
                        timestamp=datetime.utcnow()
                    )

                    embed = nextcord.Embed(
                        title=f"Update Found: {update.title}",
                        description=update.description[:4000],
                        color=0x00ff00
                    )
                    embed.add_field(name="Version", value=update.version, inline=True)
                    embed.add_field(name="Platform", value=update.platform.title(), inline=True)
                    embed.add_field(name="Game Versions", value=", ".join(update.game_versions), inline=True)
                    
                    channel = self.bot.get_channel(settings.channel_id)
                    if channel:
                        await channel.send(embed=embed)
                        settings.update_last_checked()
                        self.db.save_user_settings(ctx.guild.id, settings.__dict__)
                    
                await ctx.send("Update check complete!")
            else:
                await ctx.send("Too soon to check for updates. Please wait longer.")

def setup(bot):
    bot.add_cog(SetupCog(bot))