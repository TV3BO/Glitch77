import discord
from discord.ext import commands
import sqlite3

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', help='طرد عضو من السيرفر')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """طرد عضو"""
        if member == ctx.author:
            await ctx.send("❌ لا يمكنك طرد نفسك!")
            return
        
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✅ تم الطرد",
                description=f"تم طرد {member.mention}\n**السبب:** {reason or 'لم يتم تحديد سبب'}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ليس لدي صلاحيات كافية!")

    @commands.command(name='ban', help='حظر عضو من السيرفر')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """حظر عضو"""
        if member == ctx.author:
            await ctx.send("❌ لا يمكنك حظر نفسك!")
            return
        
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="✅ تم الحظر",
                description=f"تم حظر {member.mention}\n**السبب:** {reason or 'لم يتم تحديد سبب'}",
                color=discord.Color.dark_red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ليس لدي صلاحيات كافية!")

    @commands.command(name='unban', help='رفع الحظر عن مستخدم')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user):
        """رفع الحظر"""
        try:
            bans = await ctx.guild.bans()
            for ban in bans:
                if ban.user.name.lower() == user.lower():
                    await ctx.guild.unban(ban.user)
                    embed = discord.Embed(
                        title="✅ تم رفع الحظر",
                        description=f"تم رفع الحظر عن {ban.user.mention}",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                    return
            await ctx.send("❌ لم يتم العثور على هذا المستخدم!")
        except discord.Forbidden:
            await ctx.send("❌ ليس لدي صلاحيات كافية!")

    @commands.command(name='mute', help='إسكات عضو')
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 5, *, reason=None):
        """إسكات عضو (بالدقائق)"""
        import datetime
        
        if member == ctx.author:
            await ctx.send("❌ لا يمكنك إسكات نفسك!")
            return
        
        try:
            await member.timeout(datetime.timedelta(minutes=duration), reason=reason)
            embed = discord.Embed(
                title="🔇 تم الإسكات",
                description=f"تم إسكات {member.mention} لمدة {duration} دقيقة\n**السبب:** {reason or 'لم يتم تحديد سبب'}",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ليس لدي صلاحيات كافية!")

    @commands.command(name='unmute', help='إلغاء الإسكات')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """إلغاء الإسكات"""
        try:
            await member.timeout(None)
            embed = discord.Embed(
                title="🔊 تم إلغاء الإسكات",
                description=f"تم إلغاء الإسكات عن {member.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ ليس لدي صلاحيات كافية!")

    @commands.command(name='clear', help='حذف رسائل من القناة')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        """حذف عدد من الرسائل"""
        if amount > 100:
            await ctx.send("❌ لا يمكنك حذف أكثر من 100 رسالة!")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount)
            embed = discord.Embed(
                title="✅ تم الحذف",
                description=f"تم حذف {len(deleted)} رسالة",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed, delete_after=5)
        except discord.Forbidden:
            await ctx.send("❌ ليس لدي صلاحيات كافية!")

    @commands.command(name='warn', help='تحذير عضو')
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        """تحذير عضو"""
        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        
        c.execute('SELECT warned FROM users WHERE user_id = ? AND guild_id = ?',
                  (member.id, ctx.guild.id))
        result = c.fetchone()
        
        if result is None:
            warned = 1
            c.execute('INSERT INTO users VALUES (?, ?, 0, 1, ?)',
                      (member.id, ctx.guild.id, warned))
        else:
            warned = result[0] + 1
            c.execute('UPDATE users SET warned = ? WHERE user_id = ? AND guild_id = ?',
                      (warned, member.id, ctx.guild.id))
        
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="⚠️ تحذير",
            description=f"تم تحذير {member.mention}\n**عدد التحذيرات:** {warned}/3\n**السبب:** {reason or 'لم يتم تحديد سبب'}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        # حظر بعد 3 تحذيرات
        if warned >= 3:
            try:
                await member.ban(reason=f"تم الحظر بسبب 3 تحذيرات: {reason}")
                embed = discord.Embed(
                    title="🚫 تم الحظر",
                    description=f"تم حظر {member.mention} بسبب 3 تحذيرات",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.command(name='warnings', help='عرض التحذيرات')
    async def warnings(self, ctx, member: discord.Member = None):
        """عرض التحذيرات"""
        if member is None:
            member = ctx.author

        conn = sqlite3.connect('data/bot.db')
        c = conn.cursor()
        c.execute('SELECT warned FROM users WHERE user_id = ? AND guild_id = ?',
                  (member.id, ctx.guild.id))
        result = c.fetchone()
        conn.close()

        warned = result[0] if result else 0

        embed = discord.Embed(
            title="⚠️ التحذيرات",
            description=f"**التحذيرات:** {warned}/3",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
