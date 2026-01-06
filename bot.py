import os
import discord
import json
import asyncio
import random
from groq import Groq
from discord.ext import commands, tasks
from discord import app_commands
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
        self.start_time = datetime.now()
        
        # Load configurations from their respective files
        self.active_channel_id = self._safe_json_read("config.json", "target")
        self.log_channel_id = self._safe_json_read("data.json", "log_channel")
        
        self.processed_messages = set()
        self.personality_lines = self._load_personality_list()

    # --- JSON INFRASTRUCTURE ---
    def _safe_json_read(self, file_path, key):
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r") as f:
                return json.load(f).get(key)
        except Exception as e:
            print(f"⚠️ Read Error: {e}")
            return None

    def _save_config(self, file_path, key, value):
        data = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try: data = json.load(f)
                except: data = {}
        data[key] = value
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def _load_personality_list(self):
        try:
            with open("personality.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            print(f"❌ Personality missing: {e}")
            return ["you are absolute. sunshine vibe."]

    # --- SETUP & STATUS ---
    async def setup_hook(self):
        print("🔗 Syncing Command Tree...")
        await self.tree.sync()
        self.status_loop.start()

    @tasks.loop(minutes=10)
    async def status_loop(self):
        statuses = ["the sunset sky ☁️", "lofi beats 🎧", "new code shards ✨", "high aura vibes 🌈"]
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(statuses)))

    async def on_ready(self):
        print(f"\nENGINE READY: {self.user}")
        print(f"\nACTIVE CHAT ID: {self.active_channel_id}")
        print(f"\nLOG CHANNEL ID: {self.log_channel_id}\n")

    # --- SYSTEM LOGGING ---
    async def sys_log(self, title, content):
        if not self.log_channel_id: return
        channel = self.get_channel(self.log_channel_id)
        if channel:
            embed = discord.Embed(title=f"☁️ {title}", description=content, color=0xADDAFF, timestamp=datetime.now())
            await channel.send(embed=embed)

    # --- INFERENCE ENGINE ---
    async def handle_inference(self, message):
        async with message.channel.typing():
            try:
                # Dynamic sampling to keep tokens low
                header = self.personality_lines[:15]
                lore = random.sample(self.personality_lines[15:], min(len(self.personality_lines)-15, 20))
                prompt = "\n".join(header + lore)

                loop = asyncio.get_event_loop()
                completion = await loop.run_in_executor(
                    None, 
                    lambda: self.groq_client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": message.content}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.75,
                        presence_penalty=1.2,
                        frequency_penalty=0.9, # Repetition killer
                        max_tokens=100
                    )
                )
                
                reply = completion.choices[0].message.content.strip()
                if reply:
                    await message.reply(reply, mention_author=False)

            except Exception as e:
                print(f"❌ Inference Error: {e}")

# --- BOT INSTANCE ---
bot = AbsoluteElite()

# --- NEW COMMANDS ---

@bot.tree.command(name="chat", description="set the active channel for ai conversation.")
@app_commands.describe(channel="the channel where the bot should talk.")
async def chat_set(interaction: discord.Interaction, channel: discord.TextChannel):
    bot.active_channel_id = channel.id
    bot._save_config("config.json", "target", channel.id)
    await interaction.response.send_message(f"✨ **cyber-link established.** i will now vibe in {channel.mention}.", ephemeral=True)
    await bot.sys_log("Channel Update", f"Active chat moved to {channel.mention} by {interaction.user.name}")

@bot.tree.command(name="logs", description="set the system logging channel.")
@app_commands.describe(channel="the channel for system events and logs.")
async def logs_set(interaction: discord.Interaction, channel: discord.TextChannel):
    bot.log_channel_id = channel.id
    bot._save_config("data.json", "log_channel", channel.id)
    await interaction.response.send_message(f"🌊 **log shard set.** system data will flow to {channel.mention}.", ephemeral=True)
    # Testing the new log channel immediately
    await bot.sys_log("System Online", "Log channel successfully re-routed.")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or message.id in bot.processed_messages: return
    bot.processed_messages.add(message.id)
    
    # AI trigger logic
    if bot.active_channel_id and message.channel.id == bot.active_channel_id:
        if not message.content.startswith("!"):
            asyncio.create_task(bot.handle_inference(message))

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
