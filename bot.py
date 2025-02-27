import asyncio
import datetime
import logging
from aiogram import Bot, Dispatcher

TOKEN = "7897982272:AAGpCDtBrPzjsdT33i87dzdV1npd9lzuJM8"
CHANNEL_ID = "@testbotseaf"

# أوقات افتتاح وإغلاق الأسواق بالتوقيت العالمي (UTC)
MARKET_TIMES = {
    "الآسيوي": {"open": (23, 50), "close": (8, 50)},
    "لندن": {"open": (7, 50), "close": (16, 50)},
    "الأمريكي": {"open": (12, 50), "close": (21, 50)}
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def send_alerts():
    while True:
        now = datetime.datetime.now(datetime.UTC)
        current_time = (now.hour, now.minute)
        
        for market, times in MARKET_TIMES.items():
            if current_time == times["open"]:
                await bot.send_message(CHANNEL_ID, f"🚀✨ قناة {market} سيفتتح بعد 10 دقائق! استعد 📊💰\n\n#SA_Forex")
            elif current_time == (times["close"][0] - 1, times["close"][1]):
                await bot.send_message(CHANNEL_ID, f"⚠️🔔 تنبيه! قناة {market} سيغلق بعد 10 دقائق، تأكد من إنهاء صفقاتك! ⏳💼\n\n#SA_Forex")
            elif current_time == times["close"]:
                await bot.send_message(CHANNEL_ID, f"🔴🚪 قناة {market} أغلق الآن، نراكم في الجلسة القادمة! 📉⏳\n\n#SA_Forex")
                
        await asyncio.sleep(60)  # فحص كل دقيقة

async def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.create_task(send_alerts())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
