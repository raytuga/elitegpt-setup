
import logging
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === GÜNCELLE ===
BOT_TOKEN = '7867961745:AAHTaSDbFp01BxUj5fUO1T6XW0yh8H0jAx8'
AUTHORIZED_USER_ID = None  # İlk mesaj atan kişi olarak otomatik ayarlanacak

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global AUTHORIZED_USER_ID
    user_id = update.effective_user.id
    if AUTHORIZED_USER_ID is None:
        AUTHORIZED_USER_ID = user_id
        await update.message.reply_text(f'✅ Yetkili kullanıcı olarak kaydedildiniz: {user_id}')
    elif user_id != AUTHORIZED_USER_ID:
        await update.message.reply_text("🚫 Bu bota erişiminiz yok.")
    else:
        await update.message.reply_text("🤖 EliteGPT hazır. Mesajınızı yazın.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != AUTHORIZED_USER_ID:
        await update.message.reply_text("🚫 Bu bota erişiminiz yok.")
        return

    user_input = update.message.text.strip()

    try:
        process = subprocess.Popen(
            ['ollama', 'run', 'elitegpt'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(user_input, timeout=60)

        if stdout:
            reply = stdout.strip()
            await update.message.reply_text(reply[:4000])  # Telegram max 4096 char
        else:
            await update.message.reply_text("🤖 Cevap alınamadı.")
    except Exception as e:
        await update.message.reply_text(f"❌ Hata oluştu: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 Bot başlatıldı.")
    app.run_polling()
