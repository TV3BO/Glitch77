import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild):
        """الحصول على قناة السجلات"""
        for channel in guild.channels:
            if 'logs' in channel.name or 'سجلات' in channel.name:
                return channel
        return None

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """تسجيل حذف الرسائل"""
        if message.guild is None:
            return

        log_channel = await self.get_log_channel(message.guild)
        if log_channel is None:
            return

        embed = discord.Embed(
            title="🗑️ تم حذف رسالة",
            description=f"**المؤلف:** {message.author.mention}\n**المحتوى:** {message.content[:100]}",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"ID: {message.id}")

        try:
            await log_channel.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """تسجيل تعديل الرسائل"""
        if before.guild is None or before.content == after.content:
            return

        log_channel = await self.get_log_channel(before.guild)
        if log_channel is None:
            return

        embed = discord.Embed(
            title="✏️ تم تعديل رسالة",
            description=f"**المؤلف:** {before.author.mention}",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name="قبل", value=before.content[:100], inline=False)
        embed.add_field(name="بعد", value=after.content[:100], inline=False)
        embed.set_footer(text=f"ID: {before.id}")

        try:
            await log_channel.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """تسجيل الحظر"""
        log_channel = await self.get_log_channel(guild)
        if log_channel is None:
            return

        embed = discord.Embed(
            title="🚫 تم حظر عضو",
            description=f"**المستخدم:** {user.mention}",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )

        try:
            await log_channel.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """تسجيل رفع الحظر"""
        log_channel = await self.get_log_channel(guild)
        if log_channel is None:
            return

        embed = discord.Embed(
            title="✅ تم رفع الحظر",
            description=f"**المستخدم:** {user.mention}",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )

        try:
            await log_channel.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.command(name='setlogs', help='تعيين قناة السجلات')
    @commands.has_permissions(administrator=True)
    async def set_logs(self, ctx, channel: discord.TextChannel):
        """تعيين قناة السجلات"""
        embed = discord.Embed(
            title="✅ تم تعيين قناة السجلات",
            description=f"قناة السجلات: {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))
