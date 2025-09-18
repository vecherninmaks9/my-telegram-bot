from telegram.ext import Application, CommandHandler, MessageHandler, filters

import json

def load_resources(filename='resources.json'):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

RESOURCES = load_resources()

async def start(update, context):
    await update.message.reply_text(
        "Привет! Напиши слово или фразу для поиска ресурса."
    )

def search_resources(query):
    query = query.lower()
    results = []
    for res in RESOURCES:
        keywords = res['keywords'] + [res['name'].lower()]
        if any(query in kw.lower() for kw in keywords):
            results.append(res)
    return results

async def handle_message(update, context):
    text = update.message.text
    matches = search_resources(text)
    if not matches:
        await update.message.reply_text("Ничего не найдено по этому запросу.")
        return
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton(res['name'], url=res['url'])]
        for res in matches
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нашёл такие ресурсы:", reply_markup=reply_markup)

def main():
    app = Application.builder().token("8473436388:AAHzgKeLC7qatCaHbdNuVSeLH6UJjrhjFS0").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
