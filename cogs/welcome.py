import discord
from discord.ext import commands
import sqlite3
import os

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_init()

    def db_init(self):
        """إنشاء قاعدة البيانات"""
        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            guild_id INTEGER,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            warned INTEGER DEFAULT 0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS guilds (
            guild_id INTEGER PRIMARY KEY,
            welcome_channel INTEGER,
            log_channel INTEGER,
            mod_role INTEGER
        )''')
        conn.commit()
        conn.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ترحيب بالعضو الجديد"""
        guild = member.guild
        
        # البحث عن قناة الترحيب
        welcome_channel = None
        for channel in guild.channels:
            if 'welcome' in channel.name or 'ترحيب' in channel.name:
                welcome_channel = channel
                break
        
        if welcome_channel is None:
            welcome_channel = guild.system_channel
        
        if welcome_channel is None:
            return
        
        # إضافة العضو لقاعدة البيانات
        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO users VALUES (?, ?, 0, 1, 0)', 
                  (member.id, guild.id))
        conn.commit()
        conn.close()
        
        # رسالة الترحيب
        embed = discord.Embed(
            title=f"🎉 مرحباً في {guild.name}",
            description=f"أهلاً وسهلاً {member.mention}!\n\nنتمنى لك وقتاً طيباً معنا!",
            color=discord.Color.green()
        )
        embed.add_field(name="👥 عدد الأعضاء", value=guild.member_count, inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        
        try:
            await welcome_channel.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """توديع العضو المغادر"""
        guild = member.guild
        
        for channel in guild.channels:
            if 'goodbye' in channel.name or 'وداعا' in channel.name or 'leave' in channel.name:
                embed = discord.Embed(
                    title="👋 وداعاً",
                    description=f"لقد غادر {member.mention} السيرفر",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.avatar.url)
                
                try:
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    pass
                break

    @commands.command(name='setwelcome', help='تعيين قناة الترحيب')
    @commands.has_permissions(administrator=True)
    async def set_welcome(self, ctx, channel: discord.TextChannel):
        """تعيين قناة الترحيب"""
        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO guilds VALUES (?, ?, NULL, NULL)', 
                  (ctx.guild.id, channel.id))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(
            title="✅ تم تعيين قناة الترحيب",
            description=f"قناة الترحيب: {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
