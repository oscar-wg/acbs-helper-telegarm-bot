import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import  ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackContext, filters
from dotenv_vault import load_dotenv
import asyncio

load_dotenv()
TELEGRAM_API_TOKEN=os.getenv('TELEGRAM_API_TOKEN')
WEBHOOK_URL = os.getenv('TELEGRAM_WEBHOOK_HOST') + TELEGRAM_API_TOKEN
ACBS_HELPER_URL=os.getenv('ACBS_HELPER_URL')
bot_app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

logging.basicConfig(level=logging.INFO, format='%(name)s %(asctime)s %(levelname)s %(message)s')
logging.info('Start')

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    msg = '你的Chat ID是 %s' % str(chat_id)
    await Bot(TELEGRAM_API_TOKEN).send_message(chat_id=chat_id, text=msg)
    logging.info('reply: %s' % msg)

async def get_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = '小助手的網址是: %s' % ACBS_HELPER_URL
    await Bot(TELEGRAM_API_TOKEN).send_message(chat_id=update.effective_chat.id, text=msg)
    logging.info('reply: %s' % msg)

async def handle_text(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    text = update.message.text
    await bot_app.bot.send_message(chat_id=chat_id, text=text)

async def setup_bot():
    bot_app.add_handler(CommandHandler('chatid', get_chat_id))
    bot_app.add_handler(CommandHandler('url', get_url))
    # bot_app.add_handler(MessageHandler(filters.TEXT, handle_text))
    await bot_app.bot.setWebhook(WEBHOOK_URL)
    await bot_app.initialize()

def create_app():
    asyncio.run(setup_bot())
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/' + TELEGRAM_API_TOKEN, methods=['POST'])
async def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return 'ok'

@app.route('/', methods=['GET'])
async def hello() -> str:
    return 'hello world'

