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

channel = '-1002324319517'

answer = None
check_for_les = {}
lesson_id = None

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
        answer = "Пока не работает("
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, role)
    
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
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Выбери день недели"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, day_of_week)
        


    elif m.text.strip() == "Неотмеченные":
        
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        
        answer = "Сообщение отправлено"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.send_message(1835294966, "Отметится!")
        bot.register_next_step_handler(m, admin_menu)
        

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
                answer += f'<u><b>{i[0]}</b></u>\n{i[4]}: {i[3]} - {i[5]} {str(i[1])[:2]}:{str(i[1])[2:]} - {str(i[2])[:2]}:{str(i[2])[2:]}\n'


        bot.send_message(channel, answer, parse_mode="HTML")
        answer = "Выложил"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)



    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_menu)

        

    return True


@exch.propperWrapper()
def day_of_week(m):
    global check_for_les
    
    if m.text.strip() in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
        lst_sel = DBMS.execute_read_query(connection, DBMS.select_lessons_for_change + f'"{m.text.strip()}"')
        #print(lst_sel)

        if len(lst_sel) == 0:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание"]
            for i in lst_of_but:
                markup.add(types.KeyboardButton(i))
            
            answer = "Нет занятий"
            bot.send_message(m.chat.id, answer, reply_markup=markup)
            bot.register_next_step_handler(m, admin_menu)



        else:
            check_for_les = {}
            for i in lst_sel:
                check_for_les[i[0]] = f'{i[4]}: {i[3]} - {i[5]} {str(i[1])[:2]}:{str(i[1])[2:]} - {str(i[2])[:2]}:{str(i[2])[2:]}'

            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            lst_of_but = list(check_for_les.values())
            for i in lst_of_but:
                markup.add(types.KeyboardButton(i))

            answer = "Выбери занятие"
            bot.send_message(m.chat.id, answer, reply_markup=markup)
            bot.register_next_step_handler(m, change_lesson)

        
    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, day_of_week)


    return True


@exch.propperWrapper()
def change_lesson(m):
    global lesson_id

    if m.text.strip() in list(check_for_les.values()):
        lesson_id = next((key for key, value in check_for_les.items() if value == m.text.strip()))
        
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Место", "Преподаватель", "Вид занятия", "Время начала", "Время конца"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Что поменять?"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, change_parameter)


    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_lesson)

    return True


@exch.propperWrapper()
def change_parameter(m):
    if m.text.strip() == "Место":
        answer = "Работает только препод!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_parameter)

    elif m.text.strip() == "Преподаватель":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        DBMS.execute_query(connection, DBMS.update_teacher_id + str(lesson_id))

        answer = "Изменнено"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    elif m.text.strip() == "Вид занятия":
        answer = "Работает только препод!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_parameter)

    elif m.text.strip() == "Время начала":
        answer = "Работает только препод!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_parameter)

    elif m.text.strip() == "Время конца":
        answer = "Работает только препод!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_parameter)

    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_parameter)

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
                answer += f'{i[3]}: {i[2]} - {i[4]} {str(i[0])[:2]}:{str(i[0])[2:]} - {str(i[1])[:2]}:{str(i[1])[2:]}\n'

            

        bot.send_message(chat_id=call.from_user.id, text=answer, reply_markup=markup)
        bot.register_next_step_handler(call.message, admin_menu)


    elif action == 'CANCEL':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        bot.send_message(chat_id=call.from_user.id, text='Отмена', reply_markup=markup)
        bot.register_next_step_handler(call.message, admin_menu)

    return True




while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0, long_polling_timeout=0)
        print("success")
    except Exception as e:
        exch.printerror(e)