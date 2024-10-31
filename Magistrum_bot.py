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

# DBMS.execute_query(connection, DBMS.delete)
# DBMS.execute_query(connection, DBMS.create_lessons_table)
# DBMS.execute_query(connection, DBMS.addition_lessons)

answer = None
channel = '-1002324319517'

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')
now = datetime.now()


@exch.propperWrapper()
@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    lst_of_but = ["Преподаватель", "Администратор"]
    for i in lst_of_but:
        markup.add(types.KeyboardButton(i))
    
    answer = "Привет! Кто ты?"
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, role)
    
    return True


@exch.propperWrapper()
def role(m):
    if  m.text.strip() == "Преподаватель":
        pass
    
    elif  m.text.strip() == "Администратор":
        answer = "Введи пароль"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, password)

    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, role)

    return True


@exch.propperWrapper()    
def password(m):
    if m.text.strip() == "0000":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
    
        answer = "Hi, Надежда Борисовна!!!"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)


    else:
        answer = "Пароль неверный"
        bot.send_message(m.chat.id, answer)

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Преподаватель", "Администратор"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
    
        answer = "Кто ты?"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, role)


    return True


@exch.propperWrapper()    
def admin_menu(m):
    if m.text.strip() == "Расписание":
        answer =  "Выбери дату"
        bot.send_message(m.chat.id, answer, reply_markup=calendar.create_calendar(name=calendar_1.prefix, year=now.year, month=now.month))
        
    elif m.text.strip() == "Корректировать":
        """
        answer = "Новое время начала"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, rasp)
        """


    elif m.text.strip() == "Неотмеченные":
        """
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        
        answer = "Сообщение отправлено"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.send_message(1835294966, "Отметится!")
        bot.register_next_step_handler(m, menu)
        """

    elif m.text.strip() == "Выложить расписание":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        

        lst_sel = DBMS.execute_read_query(connection, DBMS.select_all_lessons)
        #print(lst_sel)

        if len(lst_sel) == 0:
            answer = "Нет занятий"
        
        else:
            answer = ""
            for i in lst_sel:
                answer += f'<u><b>{i[0]}</b></u>\n{i[4]}: {i[3]}\t - \t{i[5]}\t{str(i[1])[:2]}:{str(i[1])[2:]} - {str(i[2])[:2]}:{str(i[2])[2:]}\n'


        bot.send_message(channel, answer, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(m, admin_menu)



    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_menu)

        

    return True


@exch.propperWrapper()
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)

    if action == 'DAY':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = f'Вы выбрали {date.strftime("%d.%m.%Y")}'
        bot.send_message(chat_id=call.from_user.id, text=answer, reply_markup=types.ReplyKeyboardRemove())

        lst_sel = DBMS.execute_read_query(connection, DBMS.select_lessons_in_day + str(date.isoweekday()))
        #print(lst_sel)

        if len(lst_sel) == 0:
            answer = "Нет занятий"
        
        else:
            answer = ""
            for i in lst_sel:
                answer += f'{i[3]}: {i[2]}\t - \t{i[4]}\t{str(i[0])[:2]}:{str(i[0])[2:]} - {str(i[1])[:2]}:{str(i[1])[2:]}\n'

            

        bot.send_message(chat_id=call.from_user.id, text=answer, reply_markup=markup)
        bot.register_next_step_handler(call.message, admin_menu)


        """
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))


        answer = f"21 октября понедельник\nМагиструм:\n@Timahacker - {time} - 13:30 Python"
        bot.send_message(call.message.chat.id, answer, reply_markup=markup)

        dayy = date.strftime("%d")
        print(dayy)
        bot.register_next_step_handler(call.message, menu)
        """




    elif action == 'CANCEL':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        bot.send_message(chat_id=call.from_user.id, text='Отмена', reply_markup=markup)
        bot.register_next_step_handler(call.message, admin_menu)

    return True

"""
@exch.propperWrapper()    
def rasp(m):   
    global time
    time = m.text.strip()
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    lst_of_but = ["Расписание", "Корректировать", "Неотмеченные"]
    for i in lst_of_but:
        markup.add(types.KeyboardButton(i))


    answer = "Новое время установленно"
    bot.send_message(m.chat.id, answer,  reply_markup=markup)
    bot.register_next_step_handler(m, menu)

    return True
"""


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0, long_polling_timeout=0)
        print("success")
    except Exception as e:
        exch.printerror(e)