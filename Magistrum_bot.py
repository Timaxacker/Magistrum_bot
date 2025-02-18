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
# DBMS.execute_query(connection, DBMS.create_lessons_week_table)
# DBMS.execute_query(connection, DBMS.addition_teachers)

channel = '-1002324319517'

variables = {}

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')
now = datetime.now()



@exch.propperWrapper()
@bot.message_handler(commands=["start"])
def start(m, res=False):
    variables[m.from_user.id] = {'answer': None}

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    variables[m.from_user.id]['lst_of_but'] = ["Администратор", "Преподаватель"]
    for i in variables[m.from_user.id]['lst_of_but']:
        markup.add(types.KeyboardButton(i))
    
    variables[m.from_user.id]['answer'] = "Привет! Кто ты?"
    bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
    bot.register_next_step_handler(m, role)
    
    return True


@exch.propperWrapper()
def role(m):
    if m.text.strip() == "Преподаватель":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Мои занятия", "еще кнопочка", "и третья кнопка)"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Привет)"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, teacher_menu)

    elif m.text.strip() == "Администратор":
        variables[m.from_user.id]['answer'] = "Введи пароль"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, password)

    else:
        variables[m.from_user.id]['answer'] = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, role)

    return True


@exch.propperWrapper()    
def password(m):
    if m.text.strip() == "0000":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
    
        variables[m.from_user.id]['answer'] = "Hi, Надежда Борисовна!!!"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)


    else:
        variables[m.from_user.id]['answer'] = "Пароль неверный"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Администратор", "Преподаватель"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
    
        variables[m.from_user.id]['answer'] = "Кто ты?"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, role)

    return True


@exch.propperWrapper()
def teacher_menu(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    variables[m.from_user.id]['lst_of_but'] = ["Администратор", "Преподаватель"]
    for i in variables[m.from_user.id]['lst_of_but']:
        markup.add(types.KeyboardButton(i))
    
    variables[m.from_user.id]['answer'] = "=)"
    bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
    bot.register_next_step_handler(m, role)

    return True


@exch.propperWrapper()    
def admin_menu(m):
    if m.text.strip() == "Расписание":
        variables[m.from_user.id]['answer'] =  "Выбери дату"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=calendar.create_calendar(name=calendar_1.prefix, year=now.year, month=now.month))
        
    elif m.text.strip() == "Общая корректировка":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Выбери день недели"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, day_of_week)
        

    elif m.text.strip() == "Неотмеченные":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        
        variables[m.from_user.id]['answer'] = "Сообщение отправлено"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.send_message(1835294966, "Отметится!")
        bot.register_next_step_handler(m, admin_menu)
        

    elif m.text.strip() == "Выложить расписание":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Выложить", "Корректировать", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))

        variables[m.from_user.id]['answer'] = "Его надо корректировать?"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, check_schedule)


    elif m.text.strip() == "Корректировать":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Пока не работает("
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Администратор", "Преподаватель"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Кто ты?"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, role)


    else:
        variables[m.from_user.id]['answer'] = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, admin_menu)


    return True


@exch.propperWrapper()
def check_schedule(m):
    if m.text.strip() == "Выложить":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Выбери день недели"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, post_schedule)


    elif m.text.strip() == "Корректировать":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Выбери день недели"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, day_of_week)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Отмена"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)
    
    
    else:
        variables[m.from_user.id]['answer'] = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, check_schedule)
    

    return True


@exch.propperWrapper()
def post_schedule(m):
    if m.text.strip() == "Понедельник":
        variables[m.from_user.id]['day_for_post_schedule'] = 1
    elif m.text.strip() == "Вторник": 
        variables[m.from_user.id]['day_for_post_schedule'] = 2
    elif m.text.strip() == "Среда": 
        variables[m.from_user.id]['day_for_post_schedule'] = 3
    elif m.text.strip() == "Четверг": 
        variables[m.from_user.id]['day_for_post_schedule'] = 4
    elif m.text.strip() == "Пятница":
        variables[m.from_user.id]['day_for_post_schedule'] = 5
    elif m.text.strip() == "Суббота": 
        variables[m.from_user.id]['day_for_post_schedule'] = 6
    elif m.text.strip() == "Воскресенье": 
        variables[m.from_user.id]['day_for_post_schedule'] = 7 

    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Выложить", "Корректировать", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))

        variables[m.from_user.id]['answer'] = "Его надо корректировать?"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, check_schedule)
        return True

    else:
        variables[m.from_user.id]['answer'] = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, post_schedule)
        return True

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        
    for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        

    variables[m.from_user.id]['lst_sel'] = DBMS.execute_read_query(connection, DBMS.select_lessons_in_day  + str(variables[m.from_user.id]['day_for_post_schedule']))
    # print(variables[m.from_user.id]['lst_sel'])

    if len(variables[m.from_user.id]['lst_sel']) == 0:
            variables[m.from_user.id]['answer'] = "Нет занятий"
        
    else:
            variables[m.from_user.id]['day_of_week_sel'] = DBMS.execute_read_query(connection, DBMS.select_day_of_week_for_post  + str(variables[m.from_user.id]['day_for_post_schedule']))
            variables[m.from_user.id]['answer'] = f"<u><b>{variables[m.from_user.id]['day_of_week_sel'][0][0]}</b></u>\n"
            for i in variables[m.from_user.id]['lst_sel']:
                variables[m.from_user.id]['answer'] += f'{i[3]}: {i[2]} - {i[4]} {str(i[0])[:2]}:{str(i[0])[2:]} - {str(i[1])[:2]}:{str(i[1])[2:]}\n\n'


    bot.send_message(channel, variables[m.from_user.id]['answer'], parse_mode="HTML")
    variables[m.from_user.id]['answer'] = "Выложил"
    bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
    bot.register_next_step_handler(m, admin_menu)


    return True


@exch.propperWrapper()
def day_of_week(m):
    if m.text.strip() in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
        variables[m.from_user.id]['lst_sel'] = DBMS.execute_read_query(connection, DBMS.select_lessons_for_change + f'"{m.text.strip()}"')
        # print(variables[m.from_user.id]['lst_sel'])

        if len(variables[m.from_user.id]['lst_sel']) == 0:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
            for i in variables[m.from_user.id]['lst_of_but']:
                markup.add(types.KeyboardButton(i))
            
            variables[m.from_user.id]['answer'] = "Нет занятий"
            bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
            bot.register_next_step_handler(m, admin_menu)


        else:
            variables[m.from_user.id]['check_for_les'] = {}
            for i in variables[m.from_user.id]['lst_sel']:
                variables[m.from_user.id]['check_for_les'][i[0]] = f'{i[4]}: {i[3]} - {i[5]} {str(i[1])[:2]}:{str(i[1])[2:]} - {str(i[2])[:2]}:{str(i[2])[2:]}'

            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            variables[m.from_user.id]['lst_of_but'] = list(variables[m.from_user.id]['check_for_les'].values()) + ["Отмена"]
            for i in variables[m.from_user.id]['lst_of_but']:
                markup.add(types.KeyboardButton(i))

            variables[m.from_user.id]['answer'] = "Выбери занятие"
            bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
            bot.register_next_step_handler(m, change_lesson)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Отмена"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

        
    else:
        variables[m.from_user.id]['answer'] = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, day_of_week)


    return True


@exch.propperWrapper()
def change_lesson(m):
    # print(variables[m.from_user.id]['check_for_les'].values())

    if m.text.strip() in list(variables[m.from_user.id]['check_for_les'].values()):
        variables[m.from_user.id]['lesson_id'] = next((key for key, value in variables[m.from_user.id]['check_for_les'].items() if value == m.text.strip()))
        
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Место", "Преподаватель", "Вид занятия", "Время начала", "Время конца", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Что поменять?"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, change_parameter)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Отмена"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, day_of_week)


    else:
        variables[m.from_user.id]['answer'] = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_lesson)

    return True


@exch.propperWrapper()
def change_parameter(m):
    if m.text.strip() == "Место":
        variables[m.from_user.id]['lst_areas'] = DBMS.execute_read_query(connection, DBMS.select_areas_for_change)
        
        variables[m.from_user.id]['lst_of_but'] = []
        for i in variables[m.from_user.id]['lst_areas']:
            variables[m.from_user.id]['lst_of_but'].append(i[1])

        variables[m.from_user.id]['lst_of_but'].append("Отмена")

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Выбери новое место занятия"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, change_area)

    elif m.text.strip() == "Преподаватель":
        variables[m.from_user.id]['lst_teachers'] = DBMS.execute_read_query(connection, DBMS.select_teachers_for_change)
        # print(variables[m.from_user.id]['lst_teachers'])

        variables[m.from_user.id]['lst_of_but'] = []
        for i in variables[m.from_user.id]['lst_teachers']:
            variables[m.from_user.id]['lst_of_but'].append(i[2])

        variables[m.from_user.id]['lst_of_but'].append("Отмена")

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Выбери нового преподавателя"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, change_teacher)

    elif m.text.strip() == "Вид занятия":
        variables[m.from_user.id]['answer'] = "Пока не работает("
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_parameter)

    elif m.text.strip() == "Время начала":
        variables[m.from_user.id]['answer'] = "Напиши новое время начала"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_time_begin)


    elif m.text.strip() == "Время конца":
        variables[m.from_user.id]['answer'] = "Напиши новое время конца"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_time_end)


    elif m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = list(variables[m.from_user.id]['check_for_les'].values()) + ["Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Отмена"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, change_lesson)


    else:
        variables[m.from_user.id]['answer'] = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_parameter)

    return True


@exch.propperWrapper()
def change_time_begin(m):
    variables[m.from_user.id]['lst_time'] = DBMS.execute_read_query(connection, DBMS.select_time_end_for_change + str(variables[m.from_user.id]['lesson_id']))
    
    if variables[m.from_user.id]['lst_time'][0][0] - int(m.text.strip()[:2] + m.text.strip()[3:]) >= 0:
        DBMS.execute_query(connection, DBMS.update_time_begin0 + m.text.strip()[:2] + m.text.strip()[3:] + DBMS.update_time_begin1 + str(variables[m.from_user.id]['lesson_id']))
    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))

        variables[m.from_user.id]['answer'] = "Изменено"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    else:
        variables[m.from_user.id]['answer'] = "Некорректное время"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_time_begin)

    return True


@exch.propperWrapper()
def change_time_end(m):
    variables[m.from_user.id]['lst_time'] = DBMS.execute_read_query(connection, DBMS.select_time_begin_for_change + str(variables[m.from_user.id]['lesson_id']))
    
    if int(m.text.strip()[:2] + m.text.strip()[3:]) - variables[m.from_user.id]['lst_time'][0][0] >= 0:
        DBMS.execute_query(connection, DBMS.update_time_end0 + m.text.strip()[:2] + m.text.strip()[3:] + DBMS.update_time_end1 + str(variables[m.from_user.id]['lesson_id']))
    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))

        variables[m.from_user.id]['answer'] = "Изменено"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    else:
        variables[m.from_user.id]['answer'] = "Некорректное время"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_time_end)

    return True


@exch.propperWrapper()
def change_area(m):
    variables[m.from_user.id]['lst_areas'] = DBMS.execute_read_query(connection, DBMS.select_areas_for_change)
    # print(variables[m.from_user.id]['lst_areas'][0][0], variables[m.from_user.id]['lst_areas'][0][1])

    variables[m.from_user.id]['lst_of_title'] = []
    for i in variables[m.from_user.id]['lst_areas']:
        variables[m.from_user.id]['lst_of_title'].append(i[1])

    if m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Место", "Преподаватель", "Вид занятия", "Время начала", "Время конца", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Что поменять?"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, change_parameter)

    elif m.text.strip() in variables[m.from_user.id]['lst_of_title']:
        variables[m.from_user.id]['area_id'] = None
        
        for i in range(len(variables[m.from_user.id]['lst_areas'])):
            if variables[m.from_user.id]['lst_areas'][i][1] == m.text.strip():
                variables[m.from_user.id]['area_id'] = variables[m.from_user.id]['lst_areas'][i][0]
        
        DBMS.execute_query(connection, DBMS.update_area_id0 + str(variables[m.from_user.id]['area_id']) + DBMS.update_area_id1 + str(variables[m.from_user.id]['lesson_id']))
    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))

        variables[m.from_user.id]['answer'] = "Изменено"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    else:
        variables[m.from_user.id]['answer'] = "Некорректное название"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_area)

    return True


@exch.propperWrapper()
def change_teacher(m):
    variables[m.from_user.id]['lst_teachers'] = DBMS.execute_read_query(connection, DBMS.select_teachers_for_change)
    # print(variables[m.from_user.id]['lst_areas'][0][0], variables[m.from_user.id]['lst_areas'][0][1])

    variables[m.from_user.id]['lst_of_name'] = []
    for i in variables[m.from_user.id]['lst_teachers']:
        variables[m.from_user.id]['lst_of_name'].append(i[2])

    if m.text.strip() == "Отмена":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Место", "Преподаватель", "Вид занятия", "Время начала", "Время конца", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[m.from_user.id]['answer'] = "Что поменять?"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, change_parameter)

    elif m.text.strip() in variables[m.from_user.id]['lst_of_name']:
        variables[m.from_user.id]['teacher_id'] = None
        
        for i in range(len(variables[m.from_user.id]['lst_teachers'])):
            if variables[m.from_user.id]['lst_teachers'][i][2] == m.text.strip():
                variables[m.from_user.id]['teacher_id'] = variables[m.from_user.id]['lst_teachers'][i][0]
        
        DBMS.execute_query(connection, DBMS.update_teacher_id0 + str(variables[m.from_user.id]['teacher_id']) + DBMS.update_teacher_id1 + str(variables[m.from_user.id]['lesson_id']))
    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[m.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[m.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))

        variables[m.from_user.id]['answer'] = "Изменено"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)

    else:
        variables[m.from_user.id]['answer'] = "Некорректное название"
        bot.send_message(m.chat.id, variables[m.from_user.id]['answer'])
        bot.register_next_step_handler(m, change_teacher)

    return True


@exch.propperWrapper()
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)

    if action == 'DAY':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[call.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[call.from_user.id]['lst_of_but']:
            markup.add(types.KeyboardButton(i))
        
        variables[call.from_user.id]['answer'] = f'Вы выбрали {date.strftime("%d.%m.%Y")}'
        bot.send_message(chat_id=call.from_user.id, text=variables[call.from_user.id]['answer'], reply_markup=types.ReplyKeyboardRemove())

        variables[call.from_user.id]['lst_sel'] = DBMS.execute_read_query(connection, DBMS.select_lessons_in_day + str(date.isoweekday()))
        # print(variables[m.from_user.id]['lst_sel'])

        if len(variables[call.from_user.id]['lst_sel']) == 0:
            variables[call.from_user.id]['answer'] = "Нет занятий"
        
        else:
            variables[call.from_user.id]['answer'] = ""
            for i in variables[call.from_user.id]['lst_sel']:
                variables[call.from_user.id]['answer'] += f'{i[3]}: {i[2]} - {i[4]} {str(i[0])[:2]}:{str(i[0])[2:]} - {str(i[1])[:2]}:{str(i[1])[2:]}\n'

        
        bot.send_message(chat_id=call.from_user.id, text=variables[call.from_user.id]['answer'], reply_markup=markup)
        bot.register_next_step_handler(call.message, admin_menu)


    elif action == 'CANCEL':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        variables[call.from_user.id]['lst_of_but'] = ["Расписание", "Корректировать", "Неотмеченные", "Выложить расписание", "Общая корректировка", "Отмена"]
        for i in variables[call.from_user.id]['lst_of_but']:
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