import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

# 1. Professional Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('Absolute')

class AbsoluteBot(commands.Bot):
    def __init__(self):
        # Configure intents: Message Content is required for prefix commands
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None # Customizing the help command for professionalism
        )
        
        load_dotenv()
        self.openai_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    async def setup_hook(self):
        """Initializes asynchronous components before the bot starts."""
        logger.info("Initializing Absolute core systems...")

    async def on_ready(self):
        """Triggered when the bot successfully connects to Discord gateways."""
        await self.change_presence(activity=discord.Game(name="Synthesizing Intelligence"))
        logger.info(f"Absolute successfully authenticated as {self.user} (ID: {self.user.id})")

    async def on_command_error(self, ctx, error):
        """Global error handler to prevent the bot from crashing silently."""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing required parameters. Usage: `!ask [query]`")
        else:
            logger.error(f"Execution Error: {error}")
            await ctx.send("An internal processing error occurred. Please contact the administrator.")

# Instantiate the bot
bot = AbsoluteBot()

@bot.command(name="ask")
async def ask(ctx, *, prompt: str):
    """Primary interface for DeepSeek interaction."""
    async with ctx.typing():
        try:
            response = bot.openai_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are Absolute, a professional AI assistant created by Zexino."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content
            
            # Use Embeds for a more "professional" look
            embed = discord.Embed(
                description=content,
                color=discord.Color.blue()
            )
            embed.set_footer(text="Absolute Intelligence Engine | Powered by DeepSeek")
            
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"DeepSeek API Failure: {e}")
            await ctx.send("Error: Unable to reach the intelligence engine.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        logger.critical("No DISCORD_TOKEN found in environment variables.")
