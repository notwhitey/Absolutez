import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load Keys
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

# 2. Setup DeepSeek Client
client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

# 3. Setup Discord Bot (Absolute)
intents = discord.Intents.default()
intents.message_content = True  # Allows Absolute to read messages
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Absolute is online as {bot.user}')

@bot.command()
async def ask(ctx, *, question):
    """Usage: !ask What is Python?"""
    async with ctx.typing():  # Shows "Absolute is typing..."
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are Absolute, a smart Discord bot."},
                    {"role": "user", "content": question}
                ],
                stream=False
            )
            
            answer = response.choices[0].message.content
            
            # Discord has a 2000 character limit per message
            if len(answer) > 2000:
                await ctx.send(answer[:1997] + "...")
            else:
                await ctx.send(answer)

        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

bot.run(DISCORD_TOKEN)
