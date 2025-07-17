import random
import discord
from discord.ext import commands

active_games = {}

def setup(bot):
    @bot.command(name='higherlower', aliases=['hl', 'altobajo'])
    async def higher_lower(ctx, rango: str = "100"):
        """
        Inicia un juego de Alto o Bajo (Higher or Lower)
        Ejemplos:
        &higherlower       -> Rango 1-100
        &hl 500            -> Rango 1-500
        &altobajo 1000     -> Rango 1-1000
        &altobajo 50       -> Rango 1-50
        """
        if ctx.channel.id in active_games:
            del active_games[ctx.channel.id]
        
        try:
            max_range = int(rango)
            if max_range < 10 or max_range > 10000:
                await ctx.send("El rango debe estar entre 10 y 10,000")
                return
        except ValueError:
            await ctx.send("Por favor usa un número válido para el rango (ej: 100, 500, 1000)")
            return
        
        secret_number = random.randint(1, max_range)
        
        active_games[ctx.channel.id] = {
            "secret": secret_number,
            "range": max_range,
            "attempts": 0,
            "min": 1,
            "max": max_range
        }
        
        embed = discord.Embed(
            title="🎮 ¡ALTO O BAJO!",
            description=f"**He elegido un número entre 1 y {max_range}**\n\n"
                        "¡Adivina el número! Di un número entre "
                        f"**{active_games[ctx.channel.id]['min']}** y **{active_games[ctx.channel.id]['max']}**",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="¿Cómo jugar?",
            value="Escribe un número en el chat y te diré si es **ALTO** 🔼 o **BAJO** 🔽",
            inline=False
        )
        embed.set_footer(text=f"Juego iniciado por: {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
    
    @bot.listen()
    async def on_message(message):
        if message.author.bot or message.channel.id not in active_games:
            return
        
        game = active_games[message.channel.id]
        
        try:
            guess = int(message.content)
        except ValueError:
            return
        
        if guess < game["min"] or guess > game["max"]:
            await message.channel.send(
                f"⚠️ **Fuera de rango!** Debe ser entre **{game['min']}** y **{game['max']}**",
                delete_after=5
            )
            return
        
        game["attempts"] += 1
        
        if guess == game["secret"]:
            embed = discord.Embed(
                title="🎉 ¡GANASTE!",
                description=f"**{message.author.display_name}** adivinó el número secreto: **{game['secret']}**\n\n"
                            f"Intentos totales: **{game['attempts']}**",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
            embed.set_footer(text="¡Gracias por jugar!")
            await message.channel.send(embed=embed)
            del active_games[message.channel.id]
            return
        
        if guess < game["secret"]:
            game["min"] = guess + 1
            response = f"**{guess}** es BAJO 🔽\n\nEl número está entre **{game['min']}** y **{game['max']}**"
            color = discord.Color.orange()
            emoji = "🔽"
        else:
            game["max"] = guess - 1
            response = f"**{guess}** es ALTO 🔼\n\nEl número está entre **{game['min']}** y **{game['max']}**"
            color = discord.Color.red()
            emoji = "🔼"
        
        embed = discord.Embed(
            title=f"Intento #{game['attempts']} {emoji}",
            description=response,
            color=color
        )
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
        )
        
        await message.channel.send(embed=embed)