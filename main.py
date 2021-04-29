from config import TOKEN, PORT

from telegram.ext import *

from handlers import *

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


# persistence = PicklePersistence(filename='data_file')


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
job = updater.job_queue

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(arrow_handler)
dispatcher.add_handler(format_handler)
dispatcher.add_handler(book_name_handler)

# updater.start_polling()

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)

updater.bot.set_webhook("https://bookporn.herokuapp.com/" + TOKEN)
updater.idle()