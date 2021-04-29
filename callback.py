from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from config import *

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from parse_postgres import *

import json

from extra_functions_postgres import *


FORM, BOOK = range(2)


def us(update):
    with open('users.json') as file_js:
        users = set(json.load(file_js))

    if update.message.chat_id not in users:
        users.add(update.message.chat_id)
        print('count_of_users:', len(users))

        with open('users.json', 'w') as file_js:
            json.dump(list(users), file_js)



def start(update: Update, context: CallbackContext):
    tag = update.message.from_user.language_code

    if tag == 'ru':
        text = START_MESSAGE_RUS
    else:
        text = START_MESSAGE

    context.bot.send_message(chat_id=update.message.chat_id, text=text.format(update.message.from_user.username))

    us(update)

    return BOOK


def clear_chat_data(context: CallbackContext):
    context.job.context[0].pop(context.job.context[1])


def list_send(update: Update, context: CallbackContext):
    name = update.message.text

    books = find_book(name)

    if len(books) == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, your search didn't return any results")
        return

    itr = 0

    reply_markup = []
    curr_row = []

    text = ""

    context.chat_data['count'] = context.chat_data.get('count', -1) + 1
    count = context.chat_data['count']


    if 'request' not in context.chat_data:
        context.chat_data['request'] = dict()

    context.chat_data['request'][count] = books

    context.job_queue.run_once(clear_chat_data, 108000, context=(context.chat_data['request'], count))

    while itr < 10 and itr < len(books):

        book_name = books[itr][0]
        author = books[itr][1]

        text += str(itr + 1) + '. ' + book_name + '\nAuthor: ' + author + '\n'

        curr_row.append(InlineKeyboardButton(str(itr + 1), callback_data=str(count) + ' ' + str(itr)))

        if itr == 4:
            reply_markup.append(curr_row)
            curr_row = []

        itr += 1

    if len(curr_row) != 0:
        reply_markup.append(curr_row)

    text = 'Results 1-{}'.format(itr) + ' of {}'.format(len(books)) + '\n' + text


    arrows = [InlineKeyboardButton(text='⬅', callback_data='<- -1 ' + str(count)),
              InlineKeyboardButton(text='➡', callback_data='-> ' + str(itr) + ' ' + str(count))]

    reply_markup.append(arrows)
    reply_markup = InlineKeyboardMarkup(reply_markup)

    context.bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=reply_markup)

    # context.chat_data.clear()

    # print(context.chat_data['request'], context.chat_data['count'])


def arrow(update: Update, context: CallbackContext):

    callback_query_data = update.callback_query.data.split()

    itr, count = map(int, callback_query_data[1:])

    chat_id = update.callback_query.message.chat_id

    try:
        books = context.chat_data['request'][count]

    except KeyError:
        context.bot.answer_callback_query(update.callback_query.id)
        context.bot.send_message(chat_id=chat_id, text='Sorry, the button is outdated')
        return

    if itr == -1 or itr >= len(books):
        if callback_query_data[0] == '<-':
            text = 'You are already on the first page'
        else:
            text = 'You are already on the last page'

        context.bot.answer_callback_query(update.callback_query.id, text=text)

        return

    message_id = update.callback_query.message.message_id


    if callback_query_data[0] == '<-':
        reply_markup, text = left_arrow(books, itr, count)
    else:
        reply_markup, text = right_arrow(books, itr, count)


    context.bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)

    context.bot.answer_callback_query(update.callback_query.id)


def right_arrow(books, itr, count):

    text = ''

    reply_markup = []
    curr_row = []

    pnt = 0

    while pnt < 10 and itr + pnt < len(books):

        book_name = books[itr + pnt][0]
        author = books[itr + pnt][1]

        text += str(pnt + 1) + '. ' + book_name + '\nAuthor: ' + author + '\n'

        curr_row.append(InlineKeyboardButton(str(pnt + 1), callback_data=str(count) + ' ' + str(itr + pnt)))

        if pnt == 4:
            reply_markup.append(curr_row)
            curr_row = []

        pnt += 1

    if len(curr_row) != 0:
        reply_markup.append(curr_row)

    text = 'Results {}-{}'.format(itr + 1, itr + pnt) + ' of {}'.format(len(books)) + '\n' + text


    arrows = [InlineKeyboardButton(text='⬅', callback_data='<- ' + str(itr - 1) + ' ' + str(count)),
              InlineKeyboardButton(text='➡', callback_data='-> ' + str(itr + pnt) + ' ' + str(count))]

    reply_markup.append(arrows)
    reply_markup = InlineKeyboardMarkup(reply_markup)

    return(reply_markup, text)


def left_arrow(books, itr, count):

    text = ''

    reply_markup = []
    curr_row = []

    pnt = 9

    while pnt >= 0:

        book_name = books[itr - pnt][0]
        author = books[itr - pnt][1]

        text += str(10 - pnt) + '. ' + book_name + '\nAuthor: ' + author + '\n'

        curr_row.append(InlineKeyboardButton(str(10 - pnt), callback_data=str(count) + ' ' + str(itr - pnt)))

        if itr == 5:
            reply_markup.append(curr_row)
            curr_row = []

        pnt -= 1

    if len(curr_row) != 0:
        reply_markup.append(curr_row)

    text = 'Results {}-{}'.format(itr - 8, itr + 1) + ' of {}'.format(len(books)) + '\n' + text

    arrows = [InlineKeyboardButton(text='⬅', callback_data='<- ' + str(itr - 10) + ' ' + str(count)),
              InlineKeyboardButton(text='➡', callback_data='-> ' + str(itr + 1) + ' ' + str(count))]

    reply_markup.append(arrows)
    reply_markup = InlineKeyboardMarkup(reply_markup)

    return (reply_markup, text)


def form_send(update: Update, context: CallbackContext):

    id = update.callback_query.message.chat_id

    count, itr = map(int, update.callback_query.data.split())

    callback_data = ' ' + str(count) + ' ' + str(itr)

    context.bot.answer_callback_query(update.callback_query.id)

    try:
        # if context.chat_data['request'][count][itr][2][-3:] == 'fb2':

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='FB2', callback_data='f' + callback_data)]])

        context.bot.send_message(chat_id=id, text="Choose format of the book",
                                 reply_markup=reply_markup)
        return

    except KeyError:
        context.bot.send_message(chat_id=id, text='Sorry, the button is outdated')
        return


    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='ePub', callback_data='e' + callback_data)],
                    [InlineKeyboardButton(text='FB2', callback_data='f' + callback_data)],
                    [InlineKeyboardButton(text='Mobi', callback_data='m' + callback_data)]])

    context.bot.send_message(chat_id=id, text="Choose format of the book", reply_markup=reply_markup)


def book_send(update: Update, context: CallbackContext):

    id = update.callback_query.message.chat_id


    callback_query_data = update.callback_query.data.split()
    form = callback_query_data[0]
    count, itr = map(int, callback_query_data[1:])

    try:
        name, rowid = context.chat_data['request'][count][itr][0], context.chat_data['request'][count][itr][2]

    except KeyError:
        context.bot.answer_callback_query(update.callback_query.id)
        context.bot.send_message(chat_id=id, text='Sorry, the button is outdated')
        return

    # dir_name = './books/' + name + str(itr)
    #
    # if form == 'f':
    #     name += '.fb2'
    # elif form == 'e':
    #     name += '.epub'
    # else:
    #     name += '.mobi'

    # name = make_file(name, dir_name, rowid)

    send_file(rowid, id, name)

    # shutil.rmtree(dir_name)

    context.bot.answer_callback_query(update.callback_query.id)
