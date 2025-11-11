from dotenv import load_dotenv
import os

load_dotenv()
print("Token from .env:", os.getenv("DISCORD_TOKEN"))
