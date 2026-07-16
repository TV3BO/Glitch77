import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', help='رمي نرد')
    async def roll(self, ctx, sides: int = 6):
        result = random.randint(1, sides)
        embed = discord.Embed(
            title="🎲 النتيجة",
            description=f"**{result}**",
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)

    @commands.command(name='choose', help='اختيار عشوائي')
    async def choose(self, ctx, *choices):
        if not choices:
            await ctx.send("❌ أضف اختيارات!")
            return
        
        result = random.choice(choices)
        embed = discord.Embed(
            title="🎯 الاختيار العشوائي",
            description=f"**{result}**",
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)

    @commands.command(name='8ball', help='كرة سحرية')
    async def eight_ball(self, ctx, *, question=None):
        if not question:
            await ctx.send("❌ اسأل سؤال!")
            return
        
        answers = [
            "نعم بتأكيد ✅",
            "لا تماماً ❌",
            "ربما 🤔",
            "حتماً لا 🚫",
            "استفسر لاحقاً ⏳",
            "الآن ليس الوقت المناسب ⏰"
        ]
        
        result = random.choice(answers)
        embed = discord.Embed(
            title="🔮 الكرة السحرية",
            description=f"**{result}**",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name='coinflip', help='رمي عملة')
    async def coinflip(self, ctx):
        result = random.choice(['صورة 🪙', 'كتابة 📄'])
        embed = discord.Embed(
            title="🪙 النتيجة",
            description=f"**{result}**",
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
