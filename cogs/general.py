import discord
from discord.ext import commands
import os

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='عرض تأخر البوت')
    async def ping(self, ctx):
        """عرض التأخر (Ping) والاتصال"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Ping",
            description=f"**التأخر:** {latency}ms",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name='hello', help='تحية من البوت')
    async def hello(self, ctx):
        """تحية ترحيب"""
        embed = discord.Embed(
            title="👋 مرحباً",
            description=f"مرحباً {ctx.author.mention}!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='user', help='عرض معلومات المستخدم')
    async def user_info(self, ctx, member: discord.Member = None):
        """عرض معلومات المستخدم"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"معلومات {member.name}",
            color=member.color
        )
        embed.add_field(name="🆔 ID", value=member.id, inline=False)
        embed.add_field(name="📅 تاريخ الإنضمام", value=member.joined_at.strftime('%Y-%m-%d'), inline=False)
        embed.add_field(name="⚠️ الرتب", value=', '.join([role.mention for role in member.roles[1:]]) or "لا توجد رتب", inline=False)
        embed.add_field(name="📊 الحالة", value=str(member.status).capitalize(), inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        
        await ctx.send(embed=embed)

    @commands.command(name='server', help='معلومات السيرفر')
    async def server_info(self, ctx):
        """عرض معلومات السيرفر"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"معلومات {guild.name}",
            color=discord.Color.purple()
        )
        embed.add_field(name="👥 عدد الأعضاء", value=guild.member_count, inline=False)
        embed.add_field(name="📺 عدد القنوات", value=len(guild.channels), inline=False)
        embed.add_field(name="🎭 عدد الرتب", value=len(guild.roles), inline=False)
        embed.add_field(name="📅 تاريخ الإنشاء", value=guild.created_at.strftime('%Y-%m-%d'), inline=False)
        embed.add_field(name="👑 المالك", value=guild.owner.mention, inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        await ctx.send(embed=embed)

    @commands.command(name='help', help='عرض جميع الأوامر')
    async def help_command(self, ctx):
        """عرض قائمة الأوامر"""
        embed = discord.Embed(
            title="📚 قائمة الأوامر",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="🎯 الأوامر العامة",
            value="`!ping` - التأخر\n`!hello` - تحية\n`!user` - معلومات المستخدم\n`!server` - معلومات السيرفر",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ أوامر الإدارة",
            value="`!kick` - طرد\n`!ban` - حظر\n`!unban` - رفع الحظر\n`!mute` - إسكات\n`!unmute` - إلغاء الإسكات\n`!clear` - حذف رسائل\n`!warn` - تحذير\n`!warnings` - عرض التحذيرات",
            inline=False
        )
        
        embed.add_field(
            name="🎮 أوامر ترفيهية",
            value="`!roll` - نرد\n`!choose` - اختيار عشوائي\n`!coinflip` - عملة\n`!8ball` - كرة سحرية\n`!say` - تكرار رسالة",
            inline=False
        )
        
        embed.add_field(
            name="📊 أوامر المستويات",
            value="`!level` - عرض مستوى\n`!leaderboard` - لوحة الصدارة",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ أوامر التكوين",
            value="`!setwelcome` - تعيين قناة الترحيب\n`!setlogs` - تعيين قناة السجلات\n`!antispam` - معلومات مكافحة الـ Spam",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='botinfo', help='معلومات البوت')
    async def bot_info(self, ctx):
        """عرض معلومات البوت"""
        embed = discord.Embed(
            title="🤖 معلومات Glitch77",
            color=discord.Color.blurple()
        )
        embed.add_field(name="📛 الاسم", value=self.bot.user.name, inline=False)
        embed.add_field(name="🆔 ID", value=self.bot.user.id, inline=False)
        embed.add_field(name="👥 عدد السيرفرات", value=len(self.bot.guilds), inline=False)
        embed.add_field(name="👤 عدد الأعضاء", value=sum(g.member_count for g in self.bot.guilds), inline=False)
        embed.add_field(name="⏱️ التأخر", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
