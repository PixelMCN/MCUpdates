import nextcord
from nextcord.ext import commands
import aiohttp
from models.models import ProjectUpdate

class ModrinthCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_base_url = "https://api.modrinth.com/v2"
        self.headers = {
            "User-Agent": "DiscordModUpdateBot/1.0"
        }

    async def fetch_updates(self, project_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_base_url}/project/{project_id}/version",
                headers=self.headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None

    @commands.command(name="modrinth_updates")
    async def modrinth_updates(self, ctx, project_id: str):
        updates = await self.fetch_updates(project_id)
        
        if updates:
            # Create an embed for the latest version
            latest = updates[0]
            update = ProjectUpdate(
                title=latest.get("name", "Unknown"),
                version=latest.get("version_number", "Unknown"),
                description=latest.get("changelog", "No changelog provided"),
                url=latest.get("downloadUrl", ""),
                platform="modrinth",
                release_type=latest.get("version_type", "release"),
                game_versions=latest.get("gameVersions", []),
                timestamp=datetime.utcnow()
            )
            embed = nextcord.Embed(
                title=f"Latest Update for {project_id}",
                color=0x00ff00
            )
            embed.add_field(
                name="Version",
                value=update.version,
                inline=True
            )
            embed.add_field(
                name="Release Type",
                value=update.release_type,
                inline=True
            )
            embed.add_field(
                name="Changelog",
                value=update.description,
                inline=False
            )
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("No updates found for this project or project doesn't exist.")

def setup(bot):
    bot.add_cog(ModrinthCog(bot))