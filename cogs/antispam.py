import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_tracker = {}  # {user_id: [(timestamp, count)]}
        self.warned_users = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        """كشف الرسائل العشوائية (Spam)"""
        if message.author.bot or message.guild is None:
            return

        user_id = message.author.id
        current_time = datetime.now()

        # تتبع الرسائل
        if user_id not in self.spam_tracker:
            self.spam_tracker[user_id] = []

        # إزالة الرسائل القديمة (أكثر من 5 ثواني)
        self.spam_tracker[user_id] = [
            (timestamp, count) for timestamp, count in self.spam_tracker[user_id]
            if current_time - timestamp < timedelta(seconds=5)
        ]

        # إضافة رسالة جديدة
        self.spam_tracker[user_id].append((current_time, 1))

        # التحقق من Spam (5 رسائل في 5 ثواني)
        if len(self.spam_tracker[user_id]) >= 5:
            await self.handle_spam(message)

    async def handle_spam(self, message):
        """معالجة الـ Spam"""
        user_id = message.author.id
        
        if user_id not in self.warned_users:
            self.warned_users[user_id] = {'count': 0, 'last_warn': datetime.now()}
        
        warn_data = self.warned_users[user_id]
        
        # إعادة تعيين العدادات إذا مضى وقت
        if datetime.now() - warn_data['last_warn'] > timedelta(hours=1):
            warn_data['count'] = 0
        
        warn_data['count'] += 1
        warn_data['last_warn'] = datetime.now()

        embed = discord.Embed(
            title="⚠️ تحذير ضد الرسائل العشوائية",
            description=f"تنبيه {message.author.mention}: لا تكرر الرسائل!\n**عدد التحذيرات:** {warn_data['count']}/3",
            color=discord.Color.orange()
        )

        try:
            await message.channel.send(embed=embed, delete_after=10)
            await message.author.send(embed=embed)
        except:
            pass

        # حظر بعد 3 تحذيرات
        if warn_data['count'] >= 3:
            try:
                embed = discord.Embed(
                    title="🚫 تم الحظر",
                    description=f"تم حظر {message.author.mention} بسبب الرسائل العشوائية المتكررة",
                    color=discord.Color.red()
                )
                await message.guild.ban(message.author, reason="رسائل عشوائية متكررة")
                await message.channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.command(name='antispam', help='تفعيل/تعطيل مكافحة الـ Spam')
    @commands.has_permissions(administrator=True)
    async def antispam(self, ctx):
        """معلومات مكافحة الـ Spam"""
        embed = discord.Embed(
            title="🛡️ نظام مكافحة الـ Spam",
            description="النظام مفعل بشكل تلقائي",
            color=discord.Color.blue()
        )
        embed.add_field(name="⚙️ القوانين", 
                       value="• 5 رسائل في 5 ثواني = تحذير\n• 3 تحذيرات = حظر", 
                       inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
