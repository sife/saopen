import asyncio
import datetime
import pytz
from aiogram import Bot, Dispatcher

# بيانات البوت
TOKEN = "7897982272:AAGpCDtBrPzjsdT33i87dzdV1npd9lzuJM8"
CHANNEL_ID = "@jordangold"

# أوقات افتتاح وإغلاق الأسواق بتوقيت الرياض (UTC+3)
MARKET_SCHEDULE = {
    "السوق الآسيوي": {"open": "04:00", "close": "10:00"},  # طوكيو
    "سوق لندن": {"open": "11:00", "close": "19:00"},
    "السوق الأمريكي": {"open": "17:30", "close": "00:00"}  # نيويورك
}

# ضبط التوقيت إلى الرياض
RIYADH_TZ = pytz.timezone("Asia/Riyadh")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_next_notification_time():
    now_riyadh = datetime.datetime.now(RIYADH_TZ).time()
    today = datetime.date.today()
    notifications = []
    
    for market, times in MARKET_SCHEDULE.items():
        open_time = datetime.datetime.strptime(times["open"], "%H:%M").time()
        close_time = datetime.datetime.strptime(times["close"], "%H:%M").time()
        
        # تنبيه قبل الافتتاح بـ 5 دقائق
        open_alert = (datetime.datetime.combine(today, open_time) - datetime.timedelta(minutes=5)).time()
        if now_riyadh < open_alert:
            notifications.append((open_alert, f"📢 {market} ستبدأ الجلسه بعد 5 دقائق!"))
        
        # تنبيه قبل الإغلاق بـ 5 دقائق
        close_alert = (datetime.datetime.combine(today, close_time) - datetime.timedelta(minutes=5)).time()
        if now_riyadh < close_alert:
            notifications.append((close_alert, f"⚠️ {market} سيغلق بعد 5 دقائق!"))
    
    notifications.sort()  # ترتيب الإشعارات حسب التوقيت
    return notifications[0] if notifications else None

async def send_notifications():
    while True:
        next_notification = get_next_notification_time()
        if next_notification:
            notify_time, message = next_notification
            now = datetime.datetime.now(RIYADH_TZ).time()
            wait_seconds = (datetime.datetime.combine(datetime.date.today(), notify_time) - 
                            datetime.datetime.combine(datetime.date.today(), now)).total_seconds()
            
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)
                await bot.send_message(CHANNEL_ID, message)
        else:
            await asyncio.sleep(60)  # إعادة التحقق كل دقيقة

async def main():
    await send_notifications()

if __name__ == "__main__":
    asyncio.run(main())
