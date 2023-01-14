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
name_user_bool = False

information = {}

list_of_vectors0 = ("https://magistrumclub.ru\n\nРобототехника Lego WeDo 2.0:\nmagistrumclub.ru/wedo\n\nScratch:\nmagistrumclub.ru/scratch\n\nРобототехника Lego Mindstorms:\nmagistrumclub.ru/legoev3\n\nСоздание сайтов:\nнет ссылка\n\n3D-моделирование:\nmagistrumclub.ru/3d-model\n\nМашинное обучение на Scratch:\nmagistrumclub.ru/machine\n\nГеймдизайн (GoDot):\nmagistrumclub.ru/godot\n\n")
list_of_vectors1 = ("Программирование на Python:\nmagistrumclub.ru/python\n\nArduino:\nmagistrumclub.ru/arduino")

list_of_affiliates0 = ("Карта с филиалами\nhttps://magistrumclub.ru/#contacts\n\nУл.Композиторов, д. 12 лит. Б (Головной центр Магиструм)\n+7 (911) 927-77-06\nmagistrumclub.ru/magistrum\n\nпр. Просвещения, д. 99\n+7 (911) 924-36-04\nmagistrumclub.ru/infinitiv\n\nул. Нахимова, д. 11\n+7 (981) 111-33-22\nmagistrumclub.ru/menar-ch\n\nул. Васенко, д. 12\n+7 (981) 249-89-97\nmagistrumclub.ru/nova\n\nул. Смоленская, д 14\n+7 (911) 916-42-10\nmagistrumclub.ru/infinitive2\n\nПр-т Королева, д. 59к2\n+7 (999) 232-26-45\nmagistrumclub.ru/centrpritazeniya\n\nул. Республиканская, д. 35\n(запись на занятия через головной центр Магиструма)\n+7 (911) 927-77-06\nmagistrumclub.ru/respublikanskaya\n\nКонстантиновский пр-т., д. 23\n+7 (911) 925-95-05\nmagistrumclub.ru/lfkrestovsky\n\nСоветская ул., 31, посёлок Песочный\n+7 (981) 335-64-93\nmagistrumclub.ru/detskayaakademianauk\n\nУл. Тельмана, 48, корп. 2\nГде телефон?\nmagistrumclub.ru/nevskogoschool\n\nУлица Дыбенко 8к2\n+7 (921) 876-73-06\nmagistrumclub.ru/kidstory")

bot = telebot.TeleBot('5365169503:AAFFmQwmbkzjuCCLN1KSD1uCEBLI33xvGpk') # API ключ бота



@bot.message_handler(commands=["start"]) # Команда для запуска бота 
def start(m, res=False): # Функция срабатывающая при старте   
    bot.send_message(m.chat.id, 'Вас приветствует Telegram бот детского роботехнического клуба "Магиструм"! Как к Вам обращаться?') # Фраза встречающая пользователя после комманды /start

    information[m.from_user.id] = []

@bot.message_handler(content_types=["text"]) # Команда для получения текста 
def name_user_func(m):
    global answer, information
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Зарегистрироваться")
    markup.add(item1)
    item2=types.KeyboardButton("Список направлений")
    markup.add(item2)
    item3=types.KeyboardButton("Список филиалов")
    markup.add(item3)
    
    if name_user_bool == False:
        information[m.from_user.id].append(m.text.strip())
    
    answer = information[m.from_user.id][0] + ', нажимайте на кнопки для дальнейших действий, иначе я Вас не пойму'
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, menu)
    
  
def menu(m): # Функция для обработки основных кнопок 
    global answer, information
    
    if m.text.strip() == 'Зарегистрироваться':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Посмотреть спиок направлений")
        markup.add(item1)
        item2=types.KeyboardButton("Я знаю нужное мне направление")
        markup.add(item2)
        
        answer = "У нас в клубе много разных направлений и перед регистрацией мы советуем Вам посмотреть спиок"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, warning)

    elif m.text.strip() == 'Список направлений':
        answer = list_of_vectors0 + list_of_vectors1
        bot.send_message(m.chat.id, answer)

        answer = "Если Вы не знаете как выбрать направление, то мы пможем: magistrumclub.ru/how"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, menu)

    elif m.text.strip() == 'Список филиалов':
        answer = list_of_affiliates0
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, menu)

    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, menu)


def warning(m):
    global answer

    if m.text.strip() == 'Посмотреть спиок направлений':
        answer = list_of_vectors0 + list_of_vectors1
        bot.send_message(m.chat.id, answer)


    answer = information[m.from_user.id][0] + ', напишите, пожалуйста, фамилию и имя ребенка ребёнка'
    bot.send_message(m.chat.id, answer)
    bot.register_next_step_handler(m, kid_name)


def kid_name(m):
    global answer, information
    
    information[m.from_user.id].append(m.text.strip())

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
    item15=types.KeyboardButton("18+")
    markup.add(item15)
    

    answer = information[m.from_user.id][0] + ', выберите, пожалуйста, возраст ребёнка'
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, kid_age)


def kid_age(m):
    global answer, information
    
    if m.text.strip() == '4' or m.text.strip() == '5' or m.text.strip() == '6' or m.text.strip() == '7' or m.text.strip() == '8' or m.text.strip() == '9' or m.text.strip() == '10' or m.text.strip() == '11' or m.text.strip() == '12' or m.text.strip() == '13' or m.text.strip() == '14' or m.text.strip() == '15' or m.text.strip() == '16' or m.text.strip() == '17' or m.text.strip() == '18+':
        information[m.from_user.id].append(int(m.text.strip()))
        
        if information[m.from_user.id][2] <= 6:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Робототехника Lego WeDo 2.0")
            markup.add(item1)

        elif information[m.from_user.id][2] >= 10:
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
            item8=types.KeyboardButton("Создание сайтов")
            markup.add(item8)
            item9=types.KeyboardButton("Разработка мобильных приложений")
            markup.add(item9)


        elif information[m.from_user.id][2] >= 9:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Разработка мобильных приложений")
            markup.add(item1)
            item2=types.KeyboardButton("Геймдизайн (GoDot)")
            markup.add(item2)
            item3=types.KeyboardButton("Машинное обучение на Scratch")
            markup.add(item3)
            item4=types.KeyboardButton("3D-моделирование")
            markup.add(item4)
            item5=types.KeyboardButton("Робототехника Lego Mindstorms")
            markup.add(item5)
            item6=types.KeyboardButton("Scratch")
            markup.add(item6)
            item7=types.KeyboardButton("Создание сайтов")
            markup.add(item7)


        elif information[m.from_user.id][2] >= 7:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Робототехника Lego Mindstorms")
            markup.add(item1)
            item2=types.KeyboardButton("Scratch")
            markup.add(item2)
        

        answer = information[m.from_user.id][0] + ', выберите, пожалуйста, направление занятий. Если в предложенных вариантах нет желаемого Вами направления, то уточните этот вопрос с администратором центра (контактные данные)'
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, vector)
        
    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, kid_age)
        

def vector(m):
    global answer, information

    if m.text.strip() == "Scratch" or m.text.strip() == "Робототехника Lego Mindstorms" or m.text.strip() == "Создание сайтов" or m.text.strip() == "3D-моделирование" or m.text.strip() == "Машинное обучение на Scratch" or m.text.strip() == "Геймдизайн (GoDot)" or m.text.strip() == "Разработка мобильных приложений" or m.text.strip() == "Arduino" or m.text.strip() == "Робототехника Lego WeDo 2.0" or m.text.strip() == "Программирование на Python":
        information[m.from_user.id].append(m.text.strip())
        
        answer = information[m.from_user.id][0] + ", собранная информация поступит администратору и он перезвонит Вам. Для этого укажите, пожалуйста, номер телефона:"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, tel_number)
    
    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, vector)


def tel_number(m):
    global answer, information

    information[m.from_user.id].append(m.text.strip())

    answer =  information[m.from_user.id][0] + ", как к Вам обращаться при звонке? (имя, отчество)"
    bot.send_message(m.chat.id, answer)
    bot.register_next_step_handler(m, name_surname)


def name_surname(m):
    global answer, information, name_user_bool

    information[m.from_user.id].append(m.text.strip())

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Ок")
    markup.add(item1)

    answer = information[m.from_user.id][0] + ", администратор перезвонит Вам, уточнит всю информацию, окончательно зарегистрирует ребенка и даст дальнейшие указания"
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    
    answer = str(information[m.from_user.id])
    bot.send_message(1835294966, answer, reply_markup=markup)
    
    information[m.from_user.id] = [information[m.from_user.id][0]]
    name_user_bool = True

    bot.register_next_step_handler(m, name_user_func)




bot.polling(none_stop=True, interval=0) # Запуск бота 