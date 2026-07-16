import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات (Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Glitch77')

# إعدادات البوت
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# متغيرات عامة
bot.start_time = datetime.now()

# تحميل الأوامر من مجلد cogs
async def load_cogs():
    """تحميل جميع cogs من مجلد cogs"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'✅ تم تحميل: {filename}')
                print(f'✅ تم تحميل: {filename}')
            except Exception as e:
                logger.error(f'❌ خطأ في تحميل {filename}: {e}')
                print(f'❌ خطأ في تحميل {filename}: {e}')

@bot.event
async def on_ready():
    """عند تشغيل البوت"""
    logger.info(f'✅ البوت متصل باسم: {bot.user}')
    print(f'✅ البوت متصل باسم: {bot.user}')
    print(f'✅ البوت ID: {bot.user.id}')
    print(f'✅ عدد السيرفرات: {len(bot.guilds)}')
    
    # تعيين الحالة
    await bot.change_presence(
        activity=discord.Game(name='!help | Glitch77'),
        status=discord.Status.online
    )

@bot.event
async def on_message(message):
    """معالجة الرسائل"""
    if message.author == bot.user:
        return
    
    # تسجيل الرسائل
    logger.info(f'{message.author} ({message.author.id}): {message.content}')
    
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    """عند انضمام البوت إلى سيرفر جديد"""
    logger.info(f'✅ انضمام البوت إلى: {guild.name} ({guild.id})')
    print(f'✅ انضمام البوت إلى: {guild.name}')

@bot.event
async def on_guild_remove(guild):
    """عند مغادرة البوت لسيرفر"""
    logger.warning(f'⚠️ مغادرة البوت من: {guild.name} ({guild.id})')
    print(f'⚠️ مغادرة البوت من: {guild.name}')

@bot.event
async def on_command_error(ctx, error):
    """معالجة الأخطاء"""
    logger.error(f'خطأ في الأمر {ctx.command}: {error}')
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ ليس لديك الصلاحيات المطلوبة!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ الأمر يحتاج إلى معاملات: `!{ctx.command} [معاملات]`")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        await ctx.send(f"❌ حدث خطأ: {error}")

# تشغيل البوت
async def main():
    """تشغيل البوت الرئيسي"""
    async with bot:
        await load_cogs()
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            logger.error('❌ التوكن غير موجود في .env')
            print('❌ التوكن غير موجود في .env')
            return
        
        await bot.start(token)

if __name__ == '__main__':
    import asyncio
    logger.info('🚀 بدء تشغيل البوت...')
    print('🚀 بدء تشغيل البوت...')
    asyncio.run(main())
