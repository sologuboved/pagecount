from tkn import TOKEN
from process_input_and_output import get_count, convert_arg, produce_output

from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

PAGES, GROUP, BY_VAL = range(3)

keyboard = [[KeyboardButton(text='Yes'),
            KeyboardButton(text='No')]]
markup = ReplyKeyboardMarkup(keyboard)


def start(bot, update):
    update.message.reply_text("Key in pages")
    return PAGES


def pages(bot, update, user_data):
    text = update.message.text
    print(text)
    count = get_count(text)
    if isinstance(count, Exception):
        count = str(count)
        update.message.reply_text("{}\nTry again".format(count[0].lower() + count[1:]))
        return PAGES
    user_data['count'] = count
    update.message.reply_text("Fine!\nShall I group results?", reply_markup=markup)
    return GROUP


def group(bot, update, user_data):
    user_data['group'] = convert_arg(update.message.text)
    update.message.reply_text("Shall I sort them by value?", reply_markup=markup)
    return BY_VAL


def by_val(bot, update, user_data):
    user_data['by_val'] = convert_arg(update.message.text)
    print(user_data)
    update.message.reply_text(produce_output(**user_data))
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={PAGES: [MessageHandler(Filters.text, pages, pass_user_data=True)],
                GROUP: [RegexHandler('^(Yes|No)$', group, pass_user_data=True)],
                BY_VAL: [RegexHandler('^(Yes|No)$', by_val, pass_user_data=True)]},
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