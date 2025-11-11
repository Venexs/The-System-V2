import discord
from discord.ext import commands
from discord import app_commands, ui
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Dropdown Menu ===
class StatSelect(ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Level", value="level", emoji="🧭"),
            discord.SelectOption(label="STR", value="str", emoji="💪"),
            discord.SelectOption(label="INT", value="int", emoji="🧠"),
            discord.SelectOption(label="PER", value="per", emoji="👁️"),
            discord.SelectOption(label="VIT", value="vit", emoji="❤️"),
            discord.SelectOption(label="AGI", value="agi", emoji="⚡"),
        ]
        super().__init__(placeholder="Select a stat to compare...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        stat = self.values[0]
        embed = get_leaderboard_embed(stat)
        await interaction.response.edit_message(embed=embed)


# === View (to hold dropdown) ===
class StatSelectView(ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(StatSelect(bot))


# === Fetch and build leaderboard ===
def get_leaderboard_embed(stat_to_sort="level"):
    try:
        stats_data = supabase.table("stats").select("*").execute().data
        users_data = supabase.table("users").select("id, username").execute().data

        if not stats_data or not users_data:
            raise Exception("No data found in Supabase tables.")

        # Merge user + stats data
        leaderboard = []
        user_lookup = {u["id"]: u["username"] for u in users_data}
        for s in stats_data:
            uid = s["id"]
            username = user_lookup.get(uid, f"User {uid}")
            leaderboard.append({
                "username": username,
                **s
            })

        # Sort by selected stat
        leaderboard.sort(key=lambda x: x.get(stat_to_sort, 0), reverse=True)

        # Create styled cyberpunk embed
        embed = discord.Embed(
            title=f"🏆 LEADERBOARD — {stat_to_sort.upper()}",
            description="Ranking of top hunters in the system ⚔️",
            color=discord.Color.dark_purple()
        )
        embed.set_thumbnail(url="https://i.imgur.com/LmYB3kd.gif")  # cyberpunky animated thumb

        for i, entry in enumerate(leaderboard[:10], start=1):
            stat_value = entry.get(stat_to_sort, 0)
            embed.add_field(
                name=f"#{i} — {entry['username']}",
                value=f"**{stat_to_sort.upper()}**: `{stat_value}`",
                inline=False
            )

        embed.set_footer(text="⚙️ Use the dropdown below to compare other stats.")
        return embed

    except Exception as e:
        return discord.Embed(
            title="❌ Leaderboard Error",
            description=f"Error fetching data:\n```{e}```",
            color=discord.Color.red()
        )


# === Register command ===
def setup_leaderboard(bot):
    @bot.command(name="leaderboard")
    async def leaderboard(ctx):
        embed = get_leaderboard_embed("level")
        view = StatSelectView(bot)
        await ctx.send(embed=embed, view=view)

    @bot.command(name="testdb")
    async def test_database(ctx):
        """Quick test to verify Supabase connectivity."""
        try:
            response = supabase.table("users").select("*", count="exact").execute()
            count = len(response.data) if response.data else 0
            await ctx.send(f"✅ Connected to Supabase!\nFound **{count}** users in database.")
        except Exception as e:
            await ctx.send(f"❌ Supabase connection failed:\n```{e}```")
