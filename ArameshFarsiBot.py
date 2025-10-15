from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

# ----------- کد اصلی رمزگذاری/رمزگشایی ----------
farsi_letters = list("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")
shuffled_letters = farsi_letters.copy()

# تولید نگاشت تصادفی که هیچ حرفی به خودش تبدیل نشه
while True:
    random.shuffle(shuffled_letters)
    if all(orig != new for orig, new in zip(farsi_letters, shuffled_letters)):
        break

fun_map = {orig: new for orig, new in zip(farsi_letters, shuffled_letters)}
reverse_map = {v: k for k, v in fun_map.items()}

def encode_fun(text):
    return ''.join(fun_map.get(c, c) for c in text)

def decode_fun(text):
    return ''.join(reverse_map.get(c, c) for c in text)
# --------------------------------------------------

# ----------- توابع ربات ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! متن خودتو اینجا بفرست.\n"
        "برای رمزگذاری: F:متن\n"
        "برای رمزگشایی: A:متن\n"
        "برای خروج: Q"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if user_input.upper() == "Q" or user_input == "بازگشت به زندگی عادی":
        await update.message.reply_text("آزادی! بازگشت به زندگی عادی...")
    elif user_input.startswith("F:"):
        text = user_input[2:].strip()
        await update.message.reply_text(f"آرامش: {encode_fun(text)}")
    elif user_input.startswith("A:"):
        text = user_input[2:].strip()
        await update.message.reply_text(f"فارسی: {decode_fun(text)}")
    else:
        await update.message.reply_text("درست وارد کن دیگ: F: یا A:")

# ----------- اجرای ربات ----------
if __name__ == "__main__":
    TOKEN = "8125456787:AAE4ruWUEyo1u9Ujr3Wke589GcX29KuWsZQ"  # ← جایگزین کن
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ربات داره اجرا میشه...")
    app.run_polling()
