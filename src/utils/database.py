import sqlite3
from typing import Dict, Any
import json
import os

class Database:
    def __init__(self):
        self.db_path = "config/settings.db"
        os.makedirs("config", exist_ok=True)
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    guild_id INTEGER,
                    channel_id INTEGER,
                    project_id TEXT,
                    platform TEXT,
                    api_key TEXT,
                    last_checked TIMESTAMP,
                    PRIMARY KEY (guild_id, project_id)
                )
            ''')
            conn.commit()

    def save_user_settings(self, guild_id: int, settings: Dict[str, Any]) -> bool:
        """Save user settings to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO user_settings 
                    (guild_id, channel_id, project_id, platform, api_key, last_checked)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (
                    guild_id,
                    settings.get('channel_id'),
                    settings.get('project_id'),
                    settings.get('platform'),
                    settings.get('api_key')
                ))
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def get_user_settings(self, guild_id: int) -> Dict[str, Any]:
        """Retrieve user settings from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT channel_id, project_id, platform, api_key, last_checked
                FROM user_settings WHERE guild_id = ?
            ''', (guild_id,))
            rows = cursor.fetchall()
            return [{
                'channel_id': row[0],
                'project_id': row[1],
                'platform': row[2],
                'api_key': row[3],
                'last_checked': row[4]
            } for row in rows]

    def update_user_settings(self, guild_id: int, settings: Dict[str, Any]) -> bool:
        """Update existing user settings"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE user_settings 
                    SET channel_id = ?, api_key = ?, last_checked = CURRENT_TIMESTAMP
                    WHERE guild_id = ? AND project_id = ? AND platform = ?
                ''', (
                    settings.get('channel_id'),
                    settings.get('api_key'),
                    guild_id,
                    settings.get('project_id'),
                    settings.get('platform')
                ))
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def delete_user_settings(self, guild_id: int, project_id: str = None) -> bool:
        """Delete user settings from the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if project_id:
                    cursor.execute('DELETE FROM user_settings WHERE guild_id = ? AND project_id = ?',
                                 (guild_id, project_id))
                else:
                    cursor.execute('DELETE FROM user_settings WHERE guild_id = ?', (guild_id,))
                conn.commit()
                return True
        except sqlite3.Error:
            return False