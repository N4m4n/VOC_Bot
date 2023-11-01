from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters,MessageHandler
from telegram.constants import ParseMode
import json
from forwarder import bot
import forwarder

PM_START_TEXT = """
Hey {}, I'm {}!
I'm a bot used to forward messages from one chat to another.

To obtain a list of commands, use /help.
"""

PM_HELP_TEXT = """
Here is a list of usable commands:
 - /start : Starts the bot.
 - /help : Sends you this help message.

just send /id in private chat/group/channel and i will reply it's id.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    if not (chat and message and user):
        return

    if chat.type == "private":
        await message.reply_text(
            PM_START_TEXT.format(user.first_name, context.bot.first_name),
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply_text("I'm up and running!")


async def help(update: Update, _):
    chat = update.effective_chat
    message = update.effective_message
    if not (chat and message):
        return

    if not chat.type == "private":
        await message.reply_text("Contact me via PM to get a list of usable commands.")
    else:
        await message.reply_text(PM_HELP_TEXT)



async def new_chat_members(update: Update, context):
    chat = update.effective_chat
    message = update.effective_message
    # bot.bot.sendMessage(chat_id=data[0]['source'], text='Hello from ChatGPT!')


    if not (chat and message):
        return

    # new_members = message.new_chat_members
    # print(new_members)
    # print(message)
    # print(chat)
    
    print(chat.id)
    data = []
    with open('chat_list.json', 'r') as f:
        data = json.load(f)
    
    if(chat.id in data[0]['destination']):
        print("Chat id already present")
        return
    
    if(chat.id == data[0]['source']):
        print("My chat id")
        return
    
    data[0]['destination'].append(chat.id)
    forwarder.CONFIG = data
    with open('chat_list.json', 'w') as f:
        json.dump(data, f)
    
    await bot.bot.sendMessage(chat_id=data[0]['source'], text='Bot was added to '+chat.title+'! Chat id: '+str(chat.id))

bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("help", help))
bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_chat_members))