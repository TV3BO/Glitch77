import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_init()

    def db_init(self):
        """إنشاء جداول قاعدة البيانات"""
        if not os.path.exists('data'):
            os.makedirs('data')
        
        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            guild_id INTEGER,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            warned INTEGER DEFAULT 0
        )''')
        conn.commit()
        conn.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        """إضافة XP عند إرسال رسالة"""
        if message.author.bot or message.guild is None:
            return

        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        
        # الحصول على بيانات المستخدم
        c.execute('SELECT xp, level FROM users WHERE user_id = ? AND guild_id = ?',
                  (message.author.id, message.guild.id))
        result = c.fetchone()
        
        if result is None:
            c.execute('INSERT INTO users VALUES (?, ?, 10, 1, 0)',
                      (message.author.id, message.guild.id))
        else:
            xp, level = result
            new_xp = xp + 10
            new_level = level
            
            # حساب المستوى (كل 100 XP = مستوى واحد)
            if new_xp >= 100 * (level + 1):
                new_level = level + 1
                new_xp = 0
                
                # إشعار بالمستوى الجديد
                embed = discord.Embed(
                    title="🎉 مبروك! مستوى جديد",
                    description=f"تم الوصول للمستوى **{new_level}**",
                    color=discord.Color.gold()
                )
                try:
                    await message.channel.send(f"{message.author.mention}", embed=embed, delete_after=5)
                except:
                    pass
            
            c.execute('UPDATE users SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?',
                      (new_xp, new_level, message.author.id, message.guild.id))
        
        conn.commit()
        conn.close()

    @commands.command(name='level', help='عرض المستوى والـ XP')
    async def level(self, ctx, member: discord.Member = None):
        """عرض مستوى العضو"""
        if member is None:
            member = ctx.author

        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        c.execute('SELECT xp, level FROM users WHERE user_id = ? AND guild_id = ?',
                  (member.id, ctx.guild.id))
        result = c.fetchone()
        conn.close()

        if result is None:
            xp, level = 0, 1
        else:
            xp, level = result

        # عمل شريط التقدم
        progress_bar = '█' * (xp // 10) + '░' * (10 - xp // 10)
        
        embed = discord.Embed(
            title=f"📊 مستوى {member.name}",
            color=member.color
        )
        embed.add_field(name="🎮 المستوى", value=level, inline=True)
        embed.add_field(name="⚡ XP", value=f"{xp}/100", inline=True)
        embed.add_field(name="📈 التقدم", value=f"`{progress_bar}`", inline=False)
        embed.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=embed)

    @commands.command(name='leaderboard', help='أفضل 10 أعضاء')
    async def leaderboard(self, ctx):
        """عرض لوحة الصدارة"""
        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        c.execute('SELECT user_id, level, xp FROM users WHERE guild_id = ? ORDER BY level DESC, xp DESC LIMIT 10',
                  (ctx.guild.id,))
        results = c.fetchall()
        conn.close()

        if not results:
            await ctx.send("❌ لا توجد بيانات!")
            return

        embed = discord.Embed(
            title="🏆 لوحة الصدارة",
            color=discord.Color.gold()
        )

        for i, (user_id, level, xp) in enumerate(results, 1):
            user = ctx.guild.get_member(user_id)
            if user:
                embed.add_field(
                    name=f"{i}. {user.name}",
                    value=f"**المستوى:** {level} | **XP:** {xp}",
                    inline=False
                )

        await ctx.send(embed=embed)

import os

async def setup(bot):
    await bot.add_cog(Levels(bot))
