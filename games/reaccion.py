import discord
from discord.ext import commands
import asyncio
import random
import time

leaderboard = {}

def setup(bot):
    @bot.command(name='reaccion', aliases=['reactionrace', 'rr'])
    async def reaction_race(ctx):
        """
        ¡Carrera de reacción! Sé el primero en responder cuando diga "YA"
        """
        embed = discord.Embed(
            title="⏱️ CARRERA DE REACCIÓN",
            description="¡Prepárate! Voy a contar:\n**3... 2... 1... ¡YA!**\n\n"
                        "El primero que reaccione con 🏁 gana",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Instrucciones",
            value="Mantén tus ojos en el chat y tu dedo listo\n"
                  "¡Reacciona lo más rápido que puedas cuando veas ¡YA!",
            inline=False
        )
        embed.set_footer(text=f"Iniciado por: {ctx.author.display_name}")
        
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        
        countdown = ["3...", "2...", "1...", "¡YA!"]
        delays = [random.uniform(0.8, 1.5) for _ in range(4)]
        
        for count, delay in zip(countdown, delays):
            embed.description = f"**{count}**"
            await msg.edit(embed=embed)
            await asyncio.sleep(delay)
        
        start_time = time.time()
        
        await msg.add_reaction("🏁")
        
        def check(reaction, user):
            return (
                reaction.message.id == msg.id and
                str(reaction.emoji) == "🏁" and
                not user.bot
            )
        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
            
            reaction_time = time.time() - start_time
            
            if user.id not in leaderboard or reaction_time < leaderboard[user.id]["time"]:
                leaderboard[user.id] = {
                    "time": reaction_time,
                    "name": user.display_name
                }
            
            embed = discord.Embed(
                title="🏁 ¡GANADOR!",
                description=f"**{user.display_name}** reaccionó en **{reaction_time:.3f} segundos**",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            
            if reaction_time < 0.3:
                embed.add_field(name="¡INCREÍBLE!", value="🤯 ¡Reflejos sobrehumanos!", inline=False)
            elif reaction_time < 0.5:
                embed.add_field(name="¡IMPRESIONANTE!", value="🚀 ¡Velocidad de cohete!", inline=False)
            else:
                embed.add_field(name="¡BIEN HECHO!", value="🎉 ¡Buen tiempo de reacción!", inline=False)
            
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            await ctx.send("⌛ ¡Tiempo agotado! Nadie reaccionó a tiempo.")
    
    @bot.command(name='topreaccion', aliases=['toprr'])
    async def reaction_top(ctx):
        """Muestra los mejores tiempos de reacción"""
        if not leaderboard:
            await ctx.send("🚫 Aún no hay tiempos registrados. ¡Juega con &reaccion!")
            return
        
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["time"])
        
        embed = discord.Embed(
            title="🏆 MEJORES TIEMPOS DE REACCIÓN",
            color=discord.Color.gold()
        )
        
        for rank, (user_id, data) in enumerate(sorted_leaderboard[:10], 1):
            embed.add_field(
                name=f"#{rank} {data['name']}",
                value=f"⏱️ {data['time']:.3f} segundos",
                inline=False
            )
        
        embed.set_footer(text="¡Demuestra tus reflejos con &reaccion!")
        await ctx.send(embed=embed)