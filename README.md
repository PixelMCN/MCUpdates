# README.md

# Discord Mod Updates Bot

This project is a Discord bot built using Nextcord that displays project updates in a channel using the Modrinth and CurseForge APIs. The bot allows users to set it up directly from the Discord client.

## Features

- Fetches and displays project updates from Modrinth and CurseForge.
- User-friendly setup commands through Discord.
- Configurable settings for API keys and other preferences.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/discord-mod-updates-bot.git
   cd discord-mod-updates-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Rename `config/config.json.example` to `config/config.json` and fill in your API keys and settings.
   - Create a `.env` file based on the `.env.example` file to set your environment variables.

4. Run the bot:
   ```
   python src/bot.py
   ```

## Usage

- Use the setup commands in Discord to configure the bot.
- The bot will automatically fetch updates from the specified APIs and post them in the designated channel.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.