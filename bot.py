import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")

orders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n\n"
        "To'y videongiz holati haqida bilish uchun\n"
        "📅 To'y sanangizni yozing:\n\n"
        "Masalan: 15.06.2025"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text in orders:
        order = orders[text]
        holat = order["holat"]
        ism = order["ism"]

        if holat == "Tayyor":
            emoji = "✅"
            xabar = "Videongiz tayyor! Biz bilan bog'laning."
        elif holat == "Ishlanmoqda":
            emoji = "🎬"
            xabar = "Videongiz montaj jarayonida, sabr qiling."
        else:
            emoji = "⏳"
            xabar = "Videongiz hali navbatda turibdi."

        await update.message.reply_text(
            f"{emoji} {ism}\n"
            f"📅 Sana: {text}\n"
            f"📋 Holat: {holat}\n\n"
            f"{xabar}"
        )
    else:
        await update.message.reply_text(
            f"❌ {text} sanasi topilmadi.\n\n"
            "Sanani to'g'ri kiritganingizni tekshiring.\n"
            "Masalan: 15.06.2025"
        )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = int(os.environ.get("ADMIN_ID", "0"))
    if update.effective_user.id != admin_id:
        await update.message.reply_text("❌ Ruxsat yo'q.")
        return

    try:
        args = context.args
        sana = args[0]
        holat = args[1]
        ism = " ".join(args[2:])
        orders[sana] = {"ism": ism, "holat": holat}
        await update.message.reply_text(f"✅ Qo'shildi: {sana} - {ism} - {holat}")
    except:
        await update.message.reply_text(
            "Format: /add 15.06.2025 Navbatda Sardor va Malika"
        )

async def list_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = int(os.environ.get("ADMIN_ID", "0"))
    if update.effective_user.id != admin_id:
        await update.message.reply_text("❌ Ruxsat yo'q.")
        return

    if not orders:
        await update.message.reply_text("Hozircha buyurtma yo'q.")
        return

    text = "📋 Barcha buyurtmalar:\n\n"
    for sana, info in orders.items():
        text += f"📅 {sana} | {info['ism']} | {info['holat']}\n"
    await update.message.reply_text(text)

async def update_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = int(os.environ.get("ADMIN_ID", "0"))
    if update.effective_user.id != admin_id:
        await update.message.reply_text("❌ Ruxsat yo'q.")
        return

    try:
        sana = context.args[0]
        holat = context.args[1]
        if sana in orders:
            orders[sana]["holat"] = holat
            await update.message.reply_text(f"✅ Yangilandi: {sana} → {holat}")
        else:
            await update.message.reply_text("❌ Sana topilmadi.")
    except:
        await update.message.reply_text(
            "Format: /update 15.06.2025 Tayyor"
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_orders))
    app.add_handler(CommandHandler("update", update_order))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
