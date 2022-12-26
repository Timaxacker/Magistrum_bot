#Ass We Can          # Талисман кода





# Импорт библиотек
import webbrowser  # Библиотека для создания ссылок
from random import randint as r # Библиотека для генерации случайных чисел
from random import choice as c
import telebot # Библиотека для создания Telegram-бота
from telebot import types # Библиотека для создания inline кнопок
from time import sleep as s



# Определение переменных и списков
answer = '' # Переменная для ответов
channel = '@botTimalox'
name_user = ''

information = [] 

bot_input = telebot.TeleBot('5009486880:AAE0gNDOLl2pouuA4x2it_3RQOGcV29D8vw') # API ключ бота
bot_output = telebot.TeleBot('5095119695:AAFSPYO3Nz1HDqzr7njbSzxRG_cgpF1tQEY') # API ключ бота
    

@bot_input.message_handler(commands=["start"]) # Команда для запуска бота 
def start(m, res=False): # Функция срабатывающая при старте   
    bot_input.send_message(m.chat.id, 'Вас приветствует Telegram бот детского роботехнического клуба "Магиструм"! Как к Вам обращаться?', reply_markup=markup) # Фраза встречающая пользователя после комманды /start


@bot_input.message_handler(content_types=["text"]) # Команда для получения текста 
def name_user(m):
    global answer, name_user
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Зарегистрироваться")
    markup.add(item1)
    
    name_user = m.text.strip()
    
    answer = name_user + ', нажимайте на кнопки для дальнейших действий, иначе я Вас не пойму'
    bot_input.send_message(m.chat.id, answer, reply_markup=markup)
    
  
def menu(m): # Функция для обработки основных кнопок 
    global answer, channel
    
    if m.text.strip() == 'Зарегистрироваться':
        answer = name_user + ', напишите, пожалуйста, имя и фамилию ребёнка'
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, kid_name)
        
    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, menu)


def kid_name(m):
    global answer, information
    
    information.append(m.text.strip())
    
    answer = name_user + ', напишите, пожалуйста, возраст ребёнка(целых лет, только цифры)'
    bot.send_message(m.chat.id, answer)
    bot.register_next_step_handler(m, kid_name)


def kid_age(m):
    global answer, information
    
    if int(m.text.strip()) < 1:
        answer = 'Вы указали возраст не корректно, попробуйте ещё раз'
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, kid_age)
    elif int(m.text.strip()) < 4 or int(m.text.strip()) > 17:
        answer = 'К сожалению, для указанного возраста нет подходящего направления. Ближайшее к вашему возрасту занятие - Lego WeDo (4+ лет)'
    information.append(m.text.strip())
    
    answer = name_user + ', напишите, пожалуйста, возраст ребёнка'
    bot.send_message(m.chat.id, answer)
    bot.register_next_step_handler(m, kid_name)
    
    
bot_input.polling(none_stop=True, interval=0) # Запуск бота 
bot_output.polling(none_stop=True, interval=0) # Запуск бота 