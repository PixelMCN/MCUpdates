import nextcord
from nextcord.ext import commands
import os
import sys
from dotenv import load_dotenv

# Add the src directory to Python path for proper imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

# Get the absolute path to the cogs directory
COGS_DIR = os.path.join(os.path.dirname(__file__), 'cogs')

# Load the bot token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("No Discord token found in environment variables!")

# Initialize the bot with required intents
intents = nextcord.Intents.default()
intents.message_content = True  # Privileged intent
intents.members = True         # Privileged intent
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    
    # Load all cogs
    for filename in os.listdir(COGS_DIR):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                # Use correct import path
                cog_path = f'cogs.{filename[:-3]}'
                bot.load_extension(cog_path)
                print(f'Loaded extension: {cog_path}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e.__class__.__name__}: {str(e)}')

    print('------')
    print(f'Loaded {len(bot.cogs)} cogs')
    print('Bot is ready!')

if __name__ == '__main__':
    bot.run(TOKEN)