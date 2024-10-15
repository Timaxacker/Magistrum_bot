import telebot
from telebot import types
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
import exceptionHandler as exch
from datetime import datetime
import DBMS
import sys

bot = telebot.TeleBot(open('API.txt', 'r').read())
exch.bot = bot

connection = DBMS.create_connection(f"{sys.path[0]}/database.sqlite")

# DBMS.execute_query(connection, DBMS.create_lessons_table)
# DBMS.execute_query(connection, DBMS.create_teachers_table)
# DBMS.execute_query(connection, DBMS.create_areas_table)
# DBMS.execute_query(connection, DBMS.create_type_lesson_table)
# DBMS.execute_query(connection, DBMS.create_state_teacher_table)
# DBMS.execute_query(connection, DBMS.create_state_area_table)
# DBMS.execute_query(connection, DBMS.create_comments_table)

# DBMS.execute_query(connection, DBMS.delete)

answer = None
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')
now = datetime.now()

@exch.propperWrapper()
@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    lst_of_but = ["Расписание", "Корректировать", "Неотмеченные"]
    for i in lst_of_but:
        markup.add(types.KeyboardButton(i))
    
    answer = "Hi, Надежда Борисовна!!!"
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, menu)
    
    return True


@exch.propperWrapper()    
def menu(m):
    if m.text.strip() == "Расписание":
        answer =  "Выберите дату"
        bot.send_message(m.chat.id, answer, reply_markup=calendar.create_calendar(name=calendar_1.prefix, year=now.year, month=now.month))
        
    return True

@exch.propperWrapper()
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)

    if action == 'DAY':
        bot.send_message(chat_id=call.from_user.id, text=f'Вы выбрали {date.strftime("%d.%m.%Y")}', reply_markup=types.ReplyKeyboardRemove())

    elif action == 'CANCEL':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        bot.send_message(chat_id=call.from_user.id, text='Отмена', reply_markup=markup)
        bot.register_next_step_handler(call, menu)  # call.message

    return True





while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0, long_polling_timeout=0)
        print("success")
    except Exception as e:
        exch.printerror(e)