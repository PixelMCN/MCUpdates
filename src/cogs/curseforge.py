import nextcord
from nextcord.ext import commands
import aiohttp
import os
from models.models import ProjectUpdate

class CurseForgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_base_url = "https://api.curseforge.com/v1"
        self.headers = {
            'x-api-key': os.getenv('CURSEFORGE_API_KEY'),
            'Accept': 'application/json'
        }

    async def fetch_updates(self, project_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_base_url}/mods/{project_id}/files",
                headers=self.headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None

    @commands.command(name="curseforge_updates")
    async def curseforge_updates(self, ctx, project_id: int):
        updates = await self.fetch_updates(project_id)
        
        if updates and updates.get('data'):
            latest = updates['data'][0]
            update = ProjectUpdate(
                title=latest.get("displayName", "Unknown"),
                version=latest.get("fileName", "Unknown"),
                description=latest.get("changelog", "No changelog provided"),
                url=latest.get("downloadUrl", ""),
                platform="curseforge",
                release_type=latest.get("releaseType", "release"),
                game_versions=latest.get("gameVersions", []),
                timestamp=datetime.utcnow()
            )
            embed = nextcord.Embed(
                title=f"Latest Update for Project {project_id}",
                color=0xf16436  # CurseForge orange
            )
            embed.add_field(
                name="File Name",
                value=update.version,
                inline=True
            )
            embed.add_field(
                name="Release Type",
                value=update.release_type,
                inline=True
            )
            embed.add_field(
                name="Game Version",
                value=", ".join(update.game_versions),
                inline=True
            )
            if update.description:
                embed.add_field(
                    name="Changelog",
                    value=update.description[:1024],  # Discord embed field limit
                    inline=False
                )
            embed.url = update.url
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch updates or project doesn't exist.")

def setup(bot):
    bot.add_cog(CurseForgeCog(bot))