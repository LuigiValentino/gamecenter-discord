import discord
from discord.ext import commands
import os
import importlib

bot = commands.Bot(command_prefix='&', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

for filename in os.listdir('./games'):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        module = importlib.import_module(f'games.{module_name}')
        if hasattr(module, 'setup'):
            module.setup(bot)

bot.run('TOKEN')