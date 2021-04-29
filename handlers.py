from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from callback import *

import re

# conversation_handler = ConversationHandler(
#     entry_points=[CommandHandler('start', start)],
#
#     states={
#         BOOK: [MessageHandler(Filters.text, list_send)]
#     },
#
#     fallbacks=[CommandHandler('cancel', cancel)]
# )


start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text, list_send)
arrow_handler = CallbackQueryHandler(arrow, pattern=re.compile('(<\-|\->).+'))
format_handler = CallbackQueryHandler(book_send, pattern=re.compile('[fem].*'))
book_name_handler = CallbackQueryHandler(form_send)