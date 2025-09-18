import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# === Загрузка ресурсов ===
def load_resources(filename='resources.json'):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

RESOURCES = load_resources()

# === Основные обработчики ===

def start(update, context):
    update.message.reply_text(
        "Привет! Напиши слово или фразу, и я найду для тебя нужные ресурсы. Для поиска достаточно написать часть названия или ключевого слова."
    )

def search_resources(query):
    query = query.lower()
    results = []
    for res in RESOURCES:
        all_keywords = res['keywords'] + [res['name'].lower()]
        if any(query in kw.lower() for kw in all_keywords):
            results.append(res)
    return results

def handle_message(update, context):
    text = update.message.text
    matches = search_resources(text)
    if not matches:
        update.message.reply_text("Ничего не найдено по этому запросу.")
        return
    keyboard = [
        [InlineKeyboardButton(res['name'], url=res['url'])]
        for res in matches
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Нашёл такие ресурсы:", reply_markup=reply_markup)

def main():
    # === ВСТАВЬ СВОЙ ТОКЕН ОТ @BotFather ниже! ===
    updater = Updater("8473436388:AAHzgKeLC7qatCaHbdNuVSeLH6UJjrhjFS0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()