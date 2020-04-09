import discord
from discord.ext import commands
import requests
from api import API

class CommandsCog(commands.Cog, name="Score Kommandoer"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chall(self, ctx, *args):
        cname = ' '.join(args)
        if API().getID(cname) != 0:
            names = API().getChallScore(API().getID(cname))
            embed = discord.Embed(description=cname, color=0x50bdfe)
            for x in range (len(names)):
                embed.add_field(name=f'#{str(x+1)}', value=names[x], inline=True)
            embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}')
            await ctx.send(embed=embed)
        else:
            await ctx.send('Ingen challenge med dette navnet!')
    
    @commands.command()
    async def score(self, ctx, *args):
        if len(args) < 1:
            soup = API().getScoreBoard()
            scoreboard = []

            for x, tag in enumerate(soup.findAll('td')):
                if x < 23 and x > 2:
                    scoreboard.append(tag.text)
                if x > 23:
                    break

            embed = discord.Embed(description='Scoreboard', color=0x50bdfe)
            for x in range(10):
                embed.add_field(name=f'#{str(x+1)} ({scoreboard[x*2+1]}p)', value=scoreboard[x*2], inline=True)
            embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}')
            await ctx.send(embed=embed)
        else:
            p_name = ' '.join(args)
            soup = API().getScoreBoard()
            next_one = False
            score = ''

            for tag in soup.findAll('td'):
                name = tag.text.lower().find(f'\t{p_name.lower()}\n')
                if next_one:
                    score = tag.text
                    next_one = False
                    break
                if name != -1:
                    p_name = tag.text
                    next_one = True

            if score != '':
                embed = discord.Embed(description='Points', color=0x50bdfe)
                embed.add_field(name=p_name, value=score, inline=True)
                embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}')
                await ctx.send(embed=embed)
            else:
                await ctx.send('Ingen bruker med dette navnet!')

def setup(bot):
    bot.add_cog(CommandsCog(bot))