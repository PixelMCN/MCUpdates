from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class ProjectUpdate:
    """Represents a project update from either Modrinth or CurseForge"""
    title: str
    version: str
    description: str
    url: str
    platform: str
    release_type: str
    file_name: Optional[str] = None
    game_versions: List[str] = None
    timestamp: datetime = None
    downloads: int = 0

@dataclass
class UserSettings:
    """Represents user configuration for update notifications"""
    guild_id: int
    channel_id: int
    project_id: str
    platform: str
    api_key: Optional[str] = None
    notifications_enabled: bool = True
    update_frequency: int = 3600  # Default check interval in seconds
    last_checked: Optional[datetime] = None
    
    def toggle_notifications(self) -> bool:
        """Toggle notification status and return new state"""
        self.notifications_enabled = not self.notifications_enabled
        return self.notifications_enabled

    def update_last_checked(self) -> None:
        """Update the last checked timestamp"""
        self.last_checked = datetime.utcnow()

    def should_check_updates(self) -> bool:
        """Determine if it's time to check for updates"""
        if not self.last_checked:
            return True
        elapsed = (datetime.utcnow() - self.last_checked).total_seconds()
        return elapsed >= self.update_frequency