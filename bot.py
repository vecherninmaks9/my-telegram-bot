from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import json

def load_resources(filename='resources.json'):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

RESOURCES = load_resources()

REPLY_KB = ReplyKeyboardMarkup([["Показать все ресурсы"]], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! 👋\n\n"
        "Я твой помощник по быстрым ссылкам. "
        "Введи ключевое слово для поиска ресурса или воспользуйся кнопкой ниже.\n"
        "Команда /all покажет все ресурсы, или просто напиши 'все'."
    )
    await update.message.reply_text(text, reply_markup=REPLY_KB)

async def all_resources(update, context):
    if not RESOURCES:
        await update.effective_message.reply_text("Список ресурсов пуст.", reply_markup=REPLY_KB)
        return
    keyboard = [
        [InlineKeyboardButton(res['name'], url=res['url'])] for res in RESOURCES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text("Все ресурсы:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_all_resources":
        await all_resources(update, context)

def search_resources(query):
    query = query.lower()
    results = []
    for res in RESOURCES:
        keywords = res['keywords'] + [res['name'].lower()]
        if any(query in kw.lower() for kw in keywords):
            results.append(res)
    return results

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if text in ("все", "все ресурсы", "показать все ресурсы"):
        await all_resources(update, context)
        return
    matches = search_resources(text)
    if not matches:
        await update.message.reply_text("Ничего не найдено по этому запросу.", reply_markup=REPLY_KB)
        return
    keyboard = [
        [InlineKeyboardButton(res['name'], url=res['url'])]
        for res in matches
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нашёл такие ресурсы:", reply_markup=reply_markup)

def main():
    app = Application.builder().token("8473436388:AAHzgKeLC7qatCaHbdNuVSeLH6UJjrhjFS0").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("all", all_resources))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()

