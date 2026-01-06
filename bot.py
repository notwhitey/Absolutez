#   _____ __________  _________________  .____     ____ ___________________________________
#  /  _  \\______   \/   _____/\_____  \ |    |   |    |   \__    ___/\_   _____/\____    /
# /  /_\  \|    |  _/\_____  \  /   |   \|    |   |    |   / |    |    |    __)_   /     / 
#/    |    \    |   \/        \/    |    \    |___|    |  /  |    |    |        \ /     /_ 
#\____|__  /______  /_______  /\_______  /_______ \______/   |____|   /_______  //_______ \
#        \/       \/        \/         \/        \/                           \/         \/


import os
import discord
import asyncio
import random
import json
from groq import Groq
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class AbsoluteElite(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        intents.members = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.log_channel_id = int(os.getenv("LOG_CHANNEL_ID", 0))
        self.active_channel_id = self._load_config()
        self.processed_messages = set()
        
        # Load personality as a list to allow "Smart Sampling"
        self.personality_lines = self._load_personality_list()

    def _load_personality_list(self):
        try:
            with open("personality.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                print(f"✨ soul synced: {len(lines)} logic lines loaded.")
                return lines
        except Exception as e:
            print(f"personality file error: {e}")
            return ["you are absolute. chill tech vibe. lowercase only."]

    def _load_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    return json.load(f).get("target")
            except: return None
        return None

    def _save_config(self, channel_id):
        with open("config.json", "w") as f:
            json.dump({"target": channel_id}, f)

    async def setup_hook(self):
        # Clears old broken commands and forces a fresh sync
        print("--- refreshing command tree ---")
        await self.tree.sync()
        print("--- system refreshed ---")

    async def on_ready(self):
        invite = f"https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=8&scope=bot%20applications.commands"
        print(f"\nENGINE ONLINE: {self.user}")
        print(f"INVITE: {invite}\n")
        await self.change_presence(activity=discord.CustomActivity(name="optimizing context shards ☁️"))

    async def process_ai_reply(self, message):
        """Logic moved inside the class to ensure 'self' is defined."""
        async with message.channel.typing():
            try:
                # SMART SAMPLING: Prevents the 413 "Request Too Large" Error
                # We take the first 15 lines (Rules) + 20 random lines (Lore)
                header = self.personality_lines[:15]
                lore = random.sample(self.personality_lines[15:], min(len(self.personality_lines)-15, 20))
                dynamic_prompt = "\n".join(header + lore)

                loop = asyncio.get_event_loop()
                completion = await loop.run_in_executor(
                    None, 
                    lambda: self.groq_client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": dynamic_prompt},
                            {"role": "user", "content": message.content}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.75,
                        presence_penalty=1.3,
                        frequency_penalty=0.8, # Kills the repetitive loops
                        max_tokens=60
                    )
                )
                
                reply = completion.choices[0].message.content.lower().strip()
                await message.reply(reply, mention_author=False)

            except Exception as e:
                print(f"engine glitch: {e}")

# ==========================================
# ==========================================
bot = AbsoluteElite()

@bot.tree.command(name="sync", description="locks absolute to this channel.")
async def sync_slash(interaction: discord.Interaction):
    bot.active_channel_id = interaction.channel_id
    bot._save_config(interaction.channel_id)
    await interaction.response.send_message("✨ frequency matched. soul locked.", ephemeral=True)

@bot.command(name="sync")
async def sync_text(ctx):
    """Backup text command in case slash commands fail."""
    bot.active_channel_id = ctx.channel.id
    bot._save_config(ctx.channel.id)
    await ctx.send("frequency matched via text protocol.")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or message.id in bot.processed_messages:
        return
    
    bot.processed_messages.add(message.id)
    if len(bot.processed_messages) > 100: bot.processed_messages.pop()

    # Process !sync command
    await bot.process_commands(message)

    if bot.active_channel_id and message.channel.id == bot.active_channel_id:
        if not message.content.startswith("!"):
            asyncio.create_task(bot.process_ai_reply(message))

bot.run(os.getenv("DISCORD_TOKEN"))
