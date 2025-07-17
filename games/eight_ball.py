import random
import discord
from discord.ext import commands

respuestas = [
    "Sí, definitivamente",
    "Es cierto",
    "Sin duda",
    "Sí",
    "Probablemente",
    "Todo apunta a que sí",
    "Parece que sí",
    "Tal vez",
    "No puedo predecirlo ahora",
    "Pregunta de nuevo más tarde",
    "No cuentes con ello",
    "Mi respuesta es no",
    "Mis fuentes dicen que no",
    "Muy dudoso",
    "No",
    "Imposible",
    "Absolutamente no",
    "Las chances son bajas",
    "Podría ser...",
    "¡Claro que sí!"
]

def setup(bot):
    @bot.command(name='pregunta', aliases=['ask', '8ball'])
    async def eight_ball(ctx, *, pregunta: str):
        """
        Haz una pregunta al bot y obtén una respuesta aleatoria
        Ejemplo: &pregunta ¿Voy a ganar la lotería?
        """
        if not pregunta.endswith('?'):
            await ctx.send("Por favor haz una pregunta terminada con '?'")
            return
        
        respuesta = random.choice(respuestas)
        
        embed = discord.Embed(
            title="🎱 BOLA MÁGICA",
            color=discord.Color.dark_purple()
        )
        
        embed.description = f"**❓ Pregunta:**\n{pregunta}"
        
        embed.add_field(
            name="✨ RESPUESTA",
            value=f"**{respuesta}**",
            inline=False
        )
        
        embed.set_author(
            name=ctx.author.display_name, 
            icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        )
        
        
        await ctx.send(embed=embed)