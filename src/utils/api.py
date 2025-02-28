import aiohttp
import os
from typing import Optional, Dict, Any

class ModAPI:
    def __init__(self):
        self.modrinth_base_url = "https://api.modrinth.com/v2"
        self.curseforge_base_url = "https://api.curseforge.com/v1"
        self.headers = {
            'User-Agent': 'ModUpdateBot/1.0',
            'Accept': 'application/json'
        }
        # Add CurseForge API key if available
        if cf_key := os.getenv('CURSEFORGE_API_KEY'):
            self.cf_headers = {**self.headers, 'x-api-key': cf_key}
        else:
            self.cf_headers = self.headers

    async def fetch_modrinth_updates(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Fetch updates from Modrinth API"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.modrinth_base_url}/project/{project_id}/version",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
            except aiohttp.ClientError:
                return None

    async def fetch_curseforge_updates(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Fetch updates from CurseForge API"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.curseforge_base_url}/mods/{project_id}/files",
                    headers=self.cf_headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
            except aiohttp.ClientError:
                return None

    async def fetch_updates(self, project_id: str, platform: str) -> Optional[Dict[str, Any]]:
        """Fetch updates based on platform"""
        if platform.lower() == "modrinth":
            return await self.fetch_modrinth_updates(project_id)
        elif platform.lower() == "curseforge":
            try:
                return await self.fetch_curseforge_updates(int(project_id))
            except ValueError:
                return None
        return None