import random
import discord
from discord.ext import commands
import asyncio

def setup(bot):
    @bot.command(name='coinflip', aliases=['flip', 'moneda'])
    async def coin_flip(ctx, lado: str = None):
        """
        Lanza una moneda al aire con animación divertida
        Ejemplos:
        &coinflip
        &flip cara
        &moneda cruz
        """
        if lado:
            lado = lado.lower()
            if lado not in ["cara", "cruz"]:
                await ctx.send("¡Elige 'cara' o 'cruz'! 🪙")
                return
        
        gifs = [
            "https://media.giphy.com/media/3ohs4kI2X9r7O8ZtoA/giphy.gif",
            "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
            "https://media.giphy.com/media/3o7buirYcmV5nSwIRW/giphy.gif",
            "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif"
        ]
        
        msg = await ctx.send("**¡Lanzando la moneda!** 🪙")
        
        for _ in range(5):
            await msg.edit(content=f"**La moneda gira...** {'☀️' if random.choice([True, False]) else '🌙'}")
            await asyncio.sleep(0.3)
        
        resultado = random.choice(["cara", "cruz"])
        resultado_emoji = "☀️ CARA" if resultado == "cara" else "🌙 CRUZ"
        
        gif_seleccionado = random.choice(gifs)
        
        embed = discord.Embed(
            title="🪙 LANZAMIENTO DE MONEDA",
            color=discord.Color.gold()
        )
        
        if lado:
            gano = (lado == resultado)
            mensaje_resultado = (
                f"¡GANASTE! 🎉" if gano else 
                f"¡Perdiste! 😢"
            )
            embed.add_field(
                name="TU ELECCIÓN",
                value="☀️ CARA" if lado == "cara" else "🌙 CRUZ",
                inline=True
            )
        else:
            mensaje_resultado = "¡Aquí está el resultado!"
        
        embed.add_field(
            name="RESULTADO",
            value=resultado_emoji,
            inline=True
        )
        
        embed.add_field(
            name="‎",
            value=mensaje_resultado,
            inline=False
        )
        
        embed.set_image(url=gif_seleccionado)
        embed.set_footer(text=f"Lanzado por: {ctx.author.display_name}")
        
        await msg.edit(content=None, embed=embed)