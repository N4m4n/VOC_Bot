from typing import Union, Optional

from telegram import Update, Message, MessageId
from telegram.error import ChatMigrated
from telegram.ext import MessageHandler, filters, ContextTypes
import requests
from forwarder import bot, REMOVE_TAG, LOGGER
from forwarder.utils import get_source, get_destenation
from os import getenv

async def send_message(
    message: Message, chat_id: int, thread_id: Optional[int] = None
) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        return await message.copy(chat_id, message_thread_id=thread_id)  # type: ignore
    return await message.forward(chat_id, message_thread_id=thread_id)  # type: ignore


async def forwarder(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    source = update.effective_chat

    if not message or not source:
        return

    report = ''
    for chat in get_destenation(message.chat_id, message.message_thread_id):
        try:
            print(chat)
            await send_message(message, chat["chat_id"], thread_id=chat["thread_id"])
            report += f"Forwarded message to {chat['chat_id']} : Success\n\n"
        except ChatMigrated as err:
            await send_message(message, err.new_chat_id)
            LOGGER.warning(
                f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!"
            )
            report += f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!\n\n"
        except Exception as err:
            LOGGER.warning(f"Failed to forward message from {source.id} to {chat} due to {err}")
            report += f"Forwarded message to {chat['chat_id']} : Failed. \nReason : {err}\n\n"
    # await message.reply_text(report)
    f = open('report.txt', 'w')
    f.write(report)
    f.close()
    BOT_TOKEN = getenv("BOT_TOKEN")
    files = {"document": open("report.txt", "rb")}
    await requests.post("https://api.telegram.org/bot" + BOT_TOKEN +"/sendDocument?chat_id=" + str(message.chat.id),files=files)

FORWARD_HANDLER = MessageHandler(
    filters.Chat([source["chat_id"] for source in get_source()])
    & ~filters.COMMAND
    & ~filters.StatusUpdate.ALL,
    forwarder,
)
bot.add_handler(FORWARD_HANDLER)
