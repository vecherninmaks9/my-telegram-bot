import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Загрузка ресурсов из файла
def load_resources(filename='ресурсы.json'):  # или 'resources.json', если у тебя так называется
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

RESOURCES = load_resources()

# Приветствие и инструкция по /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! 👋\n\n"
        "Я твой помощник по быстрым ссылкам. "
        "Просто введи слово или фразу (ключевое слово), и я найду нужный тебе ресурс.\n\n"
        "Есть команда /all — покажу все доступные ресурсы.\n"
        "Для поиска введи, например: почта, дока, support, gpt, портал и т.д."
    )
    await update.message.reply_text(text)

# Вывод всех ресурсов командой /all
async def all_resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not RESOURCES:
        await update.message.reply_text("Список ресурсов пуст.")
        return
    message = "Все ресурсы:\n\n"
    for res in RESOURCES:
        message += f"{res['name']}: {res['url']}\n"
    # Телеграм ограничен 4096 символами, разбиваем если нужно
    for i in range(0, len(message), 4000):
        await update.message.reply_text(message[i:i+4000])

# Поиск по ключевым словам
def search_resources(query):
    query = query.lower()
    results = []
    for res in RESOURCES:
        keywords = res['keywords'] + [res['name'].lower()]
        if any(query in kw.lower() for kw in keywords):
            results.append(res)
    return results

# Обработка обычных сообщений — поиск ресурса
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    matches = search_resources(text)
    if not matches:
        await update.message.reply_text("Ничего не найдено по этому запросу.")
        return
    keyboard = [
        [InlineKeyboardButton(res['name'], url=res['url'])]
        for res in matches
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нашёл такие ресурсы:", reply_markup=reply_markup)

def main():
    # ВСТАВЬ СЮДА свой токен Telegram-бота!
    app = Application.builder().token("8473436388:AAHzgKeLC7qatCaHbdNuVSeLH6UJjrhjFS0").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("all", all_resources))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
