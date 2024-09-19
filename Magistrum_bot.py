import telebot
from datetime import datetime
import exceptionHandler as exch

bot = telebot.TeleBot(open('API.txt', 'r').read())
exch.bot = bot

