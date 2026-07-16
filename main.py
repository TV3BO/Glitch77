import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Glitch77Bot')

# إعدادات البوت
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    """عند تشغيل البوت"""
    logger.info(f'✅ البوت متصل: {bot.user}')
    print(f'✅ البوت متصل: {bot.user}')
    
    # تعيين الحالة
    await bot.change_presence(
        activity=discord.Game(name='!help | Glitch77'),
        status=discord.Status.online
    )

async def load_cogs():
    """تحميل جميع الأوامر"""
    if not os.path.exists('./cogs'):
        os.makedirs('./cogs')
    
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ تم تحميل: {filename}')
            except Exception as e:
                print(f'❌ خطأ: {filename} - {e}')

async def main():
    """تشغيل البوت"""
    async with bot:
        await load_cogs()
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            print('❌ التوكن غير موجود في .env')
            return
        await bot.start(token)

if __name__ == '__main__':
    import asyncio
    print('🚀 بدء تشغيل البوت...')
    asyncio.run(main())
