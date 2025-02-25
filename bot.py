import asyncio
import datetime
import pytz
from aiogram import Bot, Dispatcher

# بيانات البوت
TOKEN = "7897982272:AAGpCDtBrPzjsdT33i87dzdV1npd9lzuJM8"
CHANNEL_ID = "@testbotseaf"

# أوقات افتتاح وإغلاق الأسواق بالتوقيت العالمي (UTC)
MARKET_SCHEDULE = {
    "السوق الآسيوي": {"open": "23:00", "close": "07:00"},  # مثال: طوكيو
    "سوق لندن": {"open": "08:00", "close": "16:00"},
    "السوق الأمريكي": {"open": "14:30", "close": "21:00"}
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_next_notification_time():
    now_utc = datetime.datetime.now(pytz.utc).time()
    today = datetime.date.today()
    notifications = []
    
    for market, times in MARKET_SCHEDULE.items():
        open_time = datetime.datetime.strptime(times["open"], "%H:%M").time()
        close_time = datetime.datetime.strptime(times["close"], "%H:%M").time()
        
        # تنبيه قبل الافتتاح بـ 5 دقائق
        open_alert = (datetime.datetime.combine(today, open_time) - datetime.timedelta(minutes=5)).time()
        if now_utc < open_alert:
            notifications.append((open_alert, f"📢 {market} سيفتتح بعد 5 دقائق!"))
        
        # تنبيه قبل الإغلاق بـ 5 دقائق
        close_alert = (datetime.datetime.combine(today, close_time) - datetime.timedelta(minutes=5)).time()
        if now_utc < close_alert:
            notifications.append((close_alert, f"⚠️ {market} سيغلق بعد 5 دقائق!"))
    
    notifications.sort()  # ترتيب الإشعارات حسب التوقيت
    return notifications[0] if notifications else None

async def send_notifications():
    while True:
        next_notification = get_next_notification_time()
        if next_notification:
            notify_time, message = next_notification
            now = datetime.datetime.now(pytz.utc).time()
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
