from tkn import TOKEN
from process_input_and_output import process_pages

from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

PAGES, GROUP, BY_VAL = range(3)

keyboard = [[KeyboardButton(text='Yes'),
            KeyboardButton(text='No')]]
markup = ReplyKeyboardMarkup(keyboard)


def start(bot, update):
    text = "Key in pages"
    update.message.reply_text(text)
    return PAGES


def pages(bot, update, user_data):
    text = update.message.text
    print(text)
    res = process_pages(text)
    if isinstance(res, Exception):
        update.message.reply_text("Try again")
        return PAGES
    else:
        update.message.reply_text("Fine! Shall I group results?", reply_markup=markup)
        user_data['res'] = res
        return GROUP


def group(bot, update, user_data):
    print('group')
    t = update.message.text
    print(t)
    update.message.reply_text("Fine! Shall group them by value?", reply_markup=markup)
    user_data['group'] = t
    return BY_VAL


def by_val(bot, update, user_data):
    print("by value")
    t = update.message.text
    print(t)
    user_data['by_val'] = t
    print(user_data)
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={PAGES: [MessageHandler(Filters.text, pages, pass_user_data=True)],
                GROUP: [RegexHandler('^(Yes|No)$', group, pass_user_data=True)],
                BY_VAL: [RegexHandler('^Yes|No$', by_val, pass_user_data=True)]},
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True, per_user=True
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()