import asyncio
import logging
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    ContextTypes, filters
)

# التوكن الحقيقي للبوت
BOT_TOKEN = "7688769259:AAFwSvFjh6wPiVuKR53t3YsLuAYOgO-nUIo"
AFFILIATE_ID = "joedeals"

# تفعيل السجل لتتبع الرسائل والأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# تحويل الرابط إلى رابط أفلييت
def convert_to_affiliate_link(url: str, affiliate_id: str) -> str:
    base_url = url.split('?')[0]
    return f"{base_url}?aff_fcid={affiliate_id}&aff_fsk=autogenCode"

# دالة معالجة الرسائل العادية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"📩 تم استقبال الرسالة: {update.message.text}")
    message_text = update.message.text.strip()
    aliexpress_pattern = r"(https?://(?:www\.)?aliexpress\.com/item/[^\s]+|https?://s\.click\.aliexpress\.com/[^\s]+)"
    match = re.search(aliexpress_pattern, message_text)

    if match:
        product_url = match.group(1)
        affiliate_url = convert_to_affiliate_link(product_url, AFFILIATE_ID)
        response = (
            f"✅ هذا هو رابط المنتج مع التخفيض عبر Joe Deals:\n{affiliate_url}\n\n"
            f"📦 استعملو تربح 💰 وعاون القناة!"
        )
    else:
        response = "🔍 أرسللي رابط منتج من AliExpress باش نعدلهولك 🔗"

    await update.message.reply_text(response)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("📥 أمر /start تم استقباله")
    await update.message.reply_text(
        "👋 مرحبا بك في بوت Joe Deals!\n"
        "أرسل رابط منتج من AliExpress وسنرجعهولك مع رابط تخفيض 🔗"
    )

# أمر /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("📥 أمر /help تم استقباله")
    await update.message.reply_text(
        "📌 طريقة الاستعمال:\n"
        "1. انسخ رابط منتج من AliExpress\n"
        "2. أرسلو هنا\n"
        "3. غادي نجاوبك برابط فيه تخفيض 🎯"
    )

# تشغيل البوت
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.initialize()
    await app.start()
    print("✅ Bot is running... اضغط Ctrl+C للإيقاف")
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("⛔ تم إيقاف البوت")
    finally:
        await app.stop()
        await app.shutdown()

# التعامل مع Python 3.14 event loop
if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except RuntimeError as e:
        if "There is no current event loop" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_bot())
        else:
            raise
