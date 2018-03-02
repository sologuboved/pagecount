from tkn import TOKEN
from process_input_and_output import get_count, convert_arg, produce_output

from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)

import logging

PAGES, GROUP, BY_VAL = range(3)

keyboard = [[KeyboardButton(text='Yes'),
             KeyboardButton(text='No')]]
markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text("Key in pages")
    return PAGES


def pages(bot, update, user_data):
    count = get_count(update.message.text)
    if isinstance(count, Exception):
        count = str(count)
        update.message.reply_text("{}\nTry again".format(count[0].upper() + count[1:]))
        return PAGES
    user_data['count'] = count
    update.message.reply_text("Fine!\nShall I group results?", reply_markup=markup)
    return GROUP


def group(bot, update, user_data):
    user_data['group'] = convert_arg(update.message.text)
    update.message.reply_text("Fine!\nShall I sort them by value?", reply_markup=markup)
    return BY_VAL


def by_val(bot, update, user_data):
    user_data['by_val'] = convert_arg(update.message.text)
    update.message.reply_text(produce_output(**user_data))
    user_data.clear()
    return ConversationHandler.END


def description(bot, update):
    reply = "This bot accepts a string of comma-separated numbers, corresponding to the beginnings of chapters, " \
            "and returns lengths of chapters. Those can be grouped and/or sorted by lengths"
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=reply)


def log_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    help_handler = CommandHandler('help', description)
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={PAGES: [MessageHandler(Filters.text, pages, pass_user_data=True)],
                GROUP: [RegexHandler('^(Yes|No)$', group, pass_user_data=True)],
                BY_VAL: [RegexHandler('^(Yes|No)$', by_val, pass_user_data=True)]},
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_error_handler(log_error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
