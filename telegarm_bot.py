import os
import logging
from telegram import Bot, Update
from telegram.ext import  ApplicationBuilder, CommandHandler, ContextTypes
from dotenv_vault import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(name)s %(asctime)s %(levelname)s %(message)s')

bot_token = os.getenv('TG_BOT_TOKEN')
 
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('receive command: %s' % 'chatid')
    chat_id = update.effective_chat.id
    msg = '您好, 觀迎使用"澳車北上小助手", 你的Chat ID是 %s, 若在網頁中設定便可收到即時信息通知' % (str(chat_id))
    await Bot(bot_token).send_message(chat_id=chat_id, text=msg)
    logging.info('reply: %s' % msg)
    
bot = ApplicationBuilder().token(bot_token).build()
bot.add_handler(CommandHandler('chatid', get_chat_id))

logging.info('bot start')
bot.run_polling()
