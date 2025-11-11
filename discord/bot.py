import discord
from discord.ext import commands
from leaderboard import setup_leaderboard  # assuming you'll define this in leaderboard.py
from dotenv import load_dotenv
import os

# Force load .env from the same folder as this file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("DISCORD_TOKEN")

# --- Load environment variables ---
load_dotenv()  # Loads variables from .env file if it exists
TOKEN = os.getenv("DISCORD_TOKEN")  # Or replace with your key directly if needed
PREFIX = "!"

# --- Set up bot ---
intents = discord.Intents.default()
intents.message_content = True  # Enable message reading for commands
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# --- Basic events ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")

# --- Load leaderboard module ---
setup_leaderboard(bot)

# --- Run bot ---
if __name__ == "__main__":
    if TOKEN is None:
        print("❌ ERROR: Discord token not found. Set DISCORD_TOKEN in your environment or .env file.")
    else:
        bot.run(TOKEN)
