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

bot = telebot.TeleBot('5365169503:AAFFmQwmbkzjuCCLN1KSD1uCEBLI33xvGpk') # API ключ бота

    

@bot.message_handler(commands=["start"]) # Команда для запуска бота 
def start(m, res=False): # Функция срабатывающая при старте   
    bot.send_message(m.chat.id, 'Вас приветствует Telegram бот детского роботехнического клуба "Магиструм"! Как к Вам обращаться?') # Фраза встречающая пользователя после комманды /start


@bot.message_handler(content_types=["text"]) # Команда для получения текста 
def name_user_func(m):
    global answer, name_user
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Зарегистрироваться")
    markup.add(item1)
    
    name_user = m.text.strip()
    
    answer = name_user + ', нажимайте на кнопки для дальнейших действий, иначе я Вас не пойму'
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, menu)
    
  
def menu(m): # Функция для обработки основных кнопок 
    global answer, channel
    
    if m.text.strip() == 'Зарегистрироваться':
        answer = name_user + ', напишите, пожалуйста, фамилию и имя ребенка ребёнка'
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, kid_name)
        
    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, menu)


def kid_name(m):
    global answer, information
    
    information.append(m.text.strip())

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("4")
    markup.add(item1)
    item2=types.KeyboardButton("5")
    markup.add(item2)
    item3=types.KeyboardButton("6")
    markup.add(item3)
    item4=types.KeyboardButton("7")
    markup.add(item4)
    item5=types.KeyboardButton("8")
    markup.add(item5)
    item6=types.KeyboardButton("9")
    markup.add(item6)
    item7=types.KeyboardButton("10")
    markup.add(item7)
    item8=types.KeyboardButton("11")
    markup.add(item8)
    item9=types.KeyboardButton("12")
    markup.add(item9)
    item10=types.KeyboardButton("13")
    markup.add(item10)
    item11=types.KeyboardButton("14")
    markup.add(item11)
    item12=types.KeyboardButton("15")
    markup.add(item12)
    item13=types.KeyboardButton("16")
    markup.add(item13)
    item14=types.KeyboardButton("17")
    markup.add(item14)
    item15=types.KeyboardButton("18 и более")
    markup.add(item15)
    

    answer = name_user + ', выберите, пожалуйста, возраст ребёнка'
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, kid_age)


def kid_age(m):
    global answer, information
    
    if m.text.strip() == '4' or m.text.strip() == '5' or m.text.strip() == '6' or m.text.strip() == '7' or m.text.strip() == '8' or m.text.strip() == '9' or m.text.strip() == '10' or m.text.strip() == '11' or m.text.strip() == '12' or m.text.strip() == '13' or m.text.strip() == '14' or m.text.strip() == '15' or m.text.strip() == '16' or m.text.strip() == '17' or m.text.strip() == '18 и более':
        information.append(int(m.text.strip()))
        
        if information[1] <= 6:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Робототехника Lego WeDo 2.0")
            markup.add(item1)

        elif information[1] >= 10:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Arduino")
            markup.add(item1)
            item2=types.KeyboardButton("Программирование на Python")
            markup.add(item2)
            item3=types.KeyboardButton("Геймдизайн")
            markup.add(item3)
            item4=types.KeyboardButton("Машинное обучение на Scratch")
            markup.add(item4)
            item5=types.KeyboardButton("3D-моделирование")
            markup.add(item5)
            item6=types.KeyboardButton("Робототехника Lego Mindstorms")
            markup.add(item6)
            item7=types.KeyboardButton("Scratch")
            markup.add(item7)

        elif information[1] >= 9:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Программирование на Python")
            markup.add(item1)
            item2=types.KeyboardButton("Геймдизайн")
            markup.add(item2)
            item3=types.KeyboardButton("Машинное обучение на Scratch")
            markup.add(item3)
            item4=types.KeyboardButton("3D-моделирование")
            markup.add(item4)
            item5=types.KeyboardButton("Робототехника Lego Mindstorms")
            markup.add(item5)
            item6=types.KeyboardButton("Scratch")
            markup.add(item6)

        elif information[1] >= 8:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("3D-моделирование")
            markup.add(item1)
            item2=types.KeyboardButton("Робототехника Lego Mindstorms")
            markup.add(item2)
            item3=types.KeyboardButton("Scratch")
            markup.add(item3)

        elif information[1] >= 7:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Робототехника Lego Mindstorms")
            markup.add(item1)
            item2=types.KeyboardButton("Scratch")
            markup.add(item2)

        elif information[1] >= 6:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Scratch")
            markup.add(item1)
        

        answer = name_user + ', выберите, пожалуйста, направление занятий. Если в предложенных вариантах нет желаемого Вами направления, то уточните этот вопрос с администратором центра (контактные данные)'
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, vector)
        
    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, kid_age)
        

def vector(m):
    global answer, information

    information.append(m.text.strip())

    print(information, "test")
    

bot.polling(none_stop=True, interval=0) # Запуск бота 