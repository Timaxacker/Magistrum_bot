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
# DBMS.execute_query(connection, DBMS.addition_teachers)

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
    lst_of_but = ["Администратор", "Преподаватель"]
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
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
    
        answer = "Hi, Надежда Борисовна!!!"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)


    else:
        answer = "Пароль неверный"
        bot.send_message(m.chat.id, answer)

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Администратор", "Преподаватель"]
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
        lst_of_but = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Выбери день недели"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, day_of_week)
        


    elif m.text.strip() == "Неотмеченные":
        
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        
        answer = "Сообщение отправлено"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.send_message(1835294966, "Отметится!")
        bot.register_next_step_handler(m, admin_menu)
        

    elif m.text.strip() == "Выложить расписание":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Выложить", "Корректировать", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = "Его надо корректировать?"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, check_schedule)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Администратор", "Преподаватель"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Кто ты?"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, role)


    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_menu)

        

    return True


@exch.propperWrapper()
def check_schedule(m):
    if m.text.strip() == "Выложить":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        

        lst_sel = DBMS.execute_read_query(connection, DBMS.select_lessons_in_day  + str(datetime.today().isoweekday()))
        # print(lst_sel)

        if len(lst_sel) == 0:
            answer = "Нет занятий"
        
        else:
            day_of_week_sel = DBMS.execute_read_query(connection, DBMS.select_day_of_week_for_post  + str(datetime.today().isoweekday()))
            answer = f'<u><b>{day_of_week_sel[0][0]}</b></u>\n'
            for i in lst_sel:
                answer += f'{i[3]}: {i[2]} - {i[4]} {str(i[0])[:2]}:{str(i[0])[2:]} - {str(i[1])[:2]}:{str(i[1])[2:]}\n\n'


        bot.send_message(channel, answer, parse_mode="HTML")
        answer = "Выложил"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)
    

    elif m.text.strip() == "Корректировать":
        day_of_week_sel = DBMS.execute_read_query(connection, DBMS.select_day_of_week_for_post  + str(datetime.today().isoweekday()))
        lst_sel = DBMS.execute_read_query(connection, DBMS.select_lessons_for_change + f'"{day_of_week_sel[0][0]}"')
        print(lst_sel)

        if len(lst_sel) == 0:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
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
            lst_of_but = list(check_for_les.values()) + ["Отмена"]
            for i in lst_of_but:
                markup.add(types.KeyboardButton(i))

            answer = "Выбери занятие"
            bot.send_message(m.chat.id, answer, reply_markup=markup)
            bot.register_next_step_handler(m, change_lesson)
    

    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Отмена"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)
    
    
    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, check_schedule)
    
    



    return True


@exch.propperWrapper()
def day_of_week(m):
    global check_for_les
    
    if m.text.strip() in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
        lst_sel = DBMS.execute_read_query(connection, DBMS.select_lessons_for_change + f'"{m.text.strip()}"')
        #print(lst_sel)

        if len(lst_sel) == 0:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
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
            lst_of_but = list(check_for_les.values()) + ["Отмена"]
            for i in lst_of_but:
                markup.add(types.KeyboardButton(i))

            answer = "Выбери занятие"
            bot.send_message(m.chat.id, answer, reply_markup=markup)
            bot.register_next_step_handler(m, change_lesson)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Отмена"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

        
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
        lst_of_but = ["Место", "Преподаватель", "Вид занятия", "Время начала", "Время конца", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Что поменять?"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, change_parameter)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Отмена"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, day_of_week)



    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_lesson)

    return True


@exch.propperWrapper()
def change_parameter(m):
    if m.text.strip() == "Место":
        lst_areas = DBMS.execute_read_query(connection, DBMS.select_areas_for_change)
        
        lst_of_but = []
        for i in lst_areas:
            lst_of_but.append(i[1])

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Выбери новое место занятия"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, change_area)

    elif m.text.strip() == "Преподаватель":
        lst_teachers = DBMS.execute_read_query(connection, DBMS.select_teachers_for_change)
        # print(lst_teachers)

        lst_of_but = []
        for i in lst_teachers:
            lst_of_but.append(i[2])

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Выбери нового преподавателя"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, change_teacher)

    elif m.text.strip() == "Вид занятия":
        answer = "Пока не работает("
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_parameter)

    elif m.text.strip() == "Время начала":
        answer = "Напиши новое время начала"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_time_begin)


    elif m.text.strip() == "Время конца":
        answer = "Напиши новое время конца"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_time_end)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = list(check_for_les.values()) + ["Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))
        
        answer = "Отмена"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, change_lesson)


    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_parameter)

    return True



@exch.propperWrapper()
def change_time_begin(m):
    lst_time = DBMS.execute_read_query(connection, DBMS.select_time_end_for_change + str(lesson_id))
    
    if lst_time[0][0] - int(m.text.strip()[:2] + m.text.strip()[3:]) >= 0:
        DBMS.execute_query(connection, DBMS.update_time_begin0 + m.text.strip()[:2] + m.text.strip()[3:] + DBMS.update_time_begin1 + str(lesson_id))
    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = "Изменено"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    else:
        answer = "Некорректное время"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_time_begin)

    return True


@exch.propperWrapper()
def change_time_end(m):
    lst_time = DBMS.execute_read_query(connection, DBMS.select_time_begin_for_change + str(lesson_id))
    
    if int(m.text.strip()[:2] + m.text.strip()[3:]) - lst_time[0][0] >= 0:
        DBMS.execute_query(connection, DBMS.update_time_end0 + m.text.strip()[:2] + m.text.strip()[3:] + DBMS.update_time_end1 + str(lesson_id))
    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = "Изменено"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    else:
        answer = "Некорректное время"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_time_end)

    return True


@exch.propperWrapper()
def change_area(m):
    lst_areas = DBMS.execute_read_query(connection, DBMS.select_areas_for_change)
    #print(lst_areas[0][0], lst_areas[0][1])

    lst_of_title = []
    for i in lst_areas:
        lst_of_title.append(i[1])

    if m.text.strip() in lst_of_title:
        area_id = None
        
        for i in range(len(lst_areas)):
            if lst_areas[i][1] == m.text.strip():
                area_id = lst_areas[i][0]
        
        DBMS.execute_query(connection, DBMS.update_area_id0 + str(area_id) + DBMS.update_area_id1 + str(lesson_id))
    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = "Изменено"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    else:
        answer = "Некорректное название"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_area)

    return True


@exch.propperWrapper()
def change_teacher(m):
    lst_teachers = DBMS.execute_read_query(connection, DBMS.select_teachers_for_change)
    #print(lst_areas[0][0], lst_areas[0][1])

    lst_of_name = []
    for i in lst_teachers:
        lst_of_name.append(i[2])

    if m.text.strip() in lst_of_name:
        teacher_id = None
        
        for i in range(len(lst_teachers)):
            if lst_teachers[i][2] == m.text.strip():
                teacher_id = lst_teachers[i][0]
        
        DBMS.execute_query(connection, DBMS.update_teacher_id0 + str(teacher_id) + DBMS.update_teacher_id1 + str(lesson_id))
    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = "Изменено"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    else:
        answer = "Некорректное название"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, change_teacher)

    return True


@exch.propperWrapper()
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)

    if action == 'DAY':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
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
        lst_of_but = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Отмена"]
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