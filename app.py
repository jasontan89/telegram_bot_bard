#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install bardapi
#!pip install telegram-text


# In[2]:


#5684873734:AAGw8VGNx0dREhr_4Z4IG3P1UtWxHmNta5Q
# !pip install pyTelegramBotAPI


# In[3]:


#get_ipython().run_line_magic('env', 'BOT_TOKEN=5684873734:AAGw8VGNx0dREhr_4Z4IG3P1UtWxHmNta5Q')


# In[4]:


import os

import telebot,time

from telegram_text import PlainText
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN')
TRANSLATE="I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. "
COMEDIAN="I want you to act as a stand-up comedian. I will provide you with some topics related to current events and you will use your wit, creativity, and observational skills to create a routine based on those topics. You should also be sure to incorporate personal anecdotes or experiences into the routine in order to make it more relatable and engaging for the audience. "
INTERVIEW="I want you to act as an interviewer. I will be the candidate and you will ask me the interview questions for the position position. I want you to only reply as the interviewer. Do not write all the conservation at once. I want you to only do the interview with me. Ask me the questions and wait for my answers. Do not write explanations. Ask me the questions one by one like an interviewer does and wait for my answers. "
bot = telebot.TeleBot(BOT_TOKEN)

import requests

# def get_daily_horoscope(sign: str, day: str) -> dict:
#     """Get daily horoscope for a zodiac sign.
#     Keyword arguments:
#     sign:str - Zodiac sign
#     day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
#     Return:dict - JSON data
#     """
#     url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
#     params = {"sign": sign, "day": day}
#     response = requests.get(url, params)

#     return response.json()


# In[5]:


BOT_TOKEN


# In[6]:


# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")
    
# @bot.message_handler(commands=['Bard'])
# def sent_msg(message):
#     bot.reply_to(message, "Proceeding to BardAPI")
    
# @bot.message_handler(commands=['horoscope'])
# def sign_handler(message):
#     text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
#     sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(sent_msg, day_handler)
    
# def day_handler(message):
#     sign = message.text
#     text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
#     sent_msg = bot.send_message(
#         message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(
#         sent_msg, fetch_horoscope, sign.capitalize())
    
# def fetch_horoscope(message, sign):
#     day = message.text
#     horoscope = get_daily_horoscope(sign, day)
#     data = horoscope["data"]
#     horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
#     bot.send_message(message.chat.id, "Here's your horoscope!")
#     bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


# In[7]:


from bardapi import Bard
import os
import requests
os.environ['_BARD_API_KEY'] = 'WQhLk4GQNBYsdSM6EJPh7bVr0nwjeLksQkmb99-ymDWiilfPrg5HFZcUKKdgywoN-1nRWQ.'
# token='xxxxxxxxxxx'

def bard_api(message):
    session = requests.Session()
    session.headers = {
                "Host": "bard.google.com",
                "X-Same-Domain": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Origin": "https://bard.google.com",
                "Referer": "https://bard.google.com/",
            }
    session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 
    # session.cookies.set("__Secure-1PSID", token) 
    #print(message)
    bard = Bard(session=session, timeout=30)
    #print(bard.get_answer(message)['content'])
    bard.get_answer("What is my last prompt??")['content']
    return str(bard.get_answer(message)['content'])

    # Continued conversation without set new session
    #bard.get_answer("What is my last prompt??")['content']


# In[8]:


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Translation')
    itembtn2 = types.KeyboardButton('Stand-up Comedian')
    itembtn3 = types.KeyboardButton('Interview Practise')
    itembtn4 = types.KeyboardButton('Normal Bard')
    markup.add(itembtn1, itembtn2, itembtn3,itembtn4)
    sent_msg = bot.send_message(message.chat.id, "Choose which services of Bard you want to use:", reply_markup=markup)
    bot.register_next_step_handler(sent_msg, options)
    
# @bot.message_handler(commands=['Bard'])
# def sent_msg(message):
#     bot.reply_to(message, "Proceeding to BardAPI")
    
# @bot.message_handler(commands=['horoscope'])
# def sign_handler(message):
#     text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
#     sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(sent_msg, day_handler)
def options(message):
    print(message.text)
    if message.text=="Translation":
        print("translate")
        sent_msg =bot.send_message(message.chat.id, "Please type in what you want to translate to English:", parse_mode="Markdown")
#         message.text= + message.text
#         print(message.text)
        bot.register_next_step_handler(sent_msg, fetch_horoscope,mode="translate")

    elif message.text=="Stand-up Comedian": 
        print("Stand-up Comedian")
        sent_msg =bot.send_message(message.chat.id, "Please type in the type of humor you like:", parse_mode="Markdown")
#         message.text= + message.text
#         print(message.text)
        bot.register_next_step_handler(sent_msg, fetch_horoscope,mode="funny")
    elif message.text=="Interview Practise":
        print("Interview Practise")
        sent_msg =bot.send_message(message.chat.id, "Please type in your first sentence in the interview:", parse_mode="Markdown")
#         message.text= + message.text
#         print(message.text)
        bot.register_next_step_handler(sent_msg, fetch_horoscope,mode="interview")
    else:
        print("Normal Bard")
        sent_msg =bot.send_message(message.chat.id, "I’m Bard, your creative and helpful collaborator. I have limitations and won’t always get it right, but your feedback will help me improve. Enter your prompt here:", parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, fetch_horoscope,mode="normal")
#     day = message.text
#     bardmsg = bard_api(day)
#     data = bardmsg
    
#     element = PlainText(data)
#     escaped_text = element.to_html()
  
#     bot.send_message(message.chat.id, "Here's your finding from Bard!")
#     bot.send_message(message.chat.id, escaped_text, parse_mode="Markdown")

@bot.message_handler(commands=['Bard'])
def day_handler(message):
    #sign = message.text
    text = "Please type the topic on what you want to know."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope)
    
def fetch_horoscope(message,mode):
    if mode=="translate":
        day = TRANSLATE + message.text
    elif mode=="funny":
        day= COMEDIAN + message.text
    elif mode=="interview":
        day=INTERVIEW+ message.text
    else:
        day=message.text
    bardmsg = bard_api(day)
    data = bardmsg
    
    element = PlainText(data)
    escaped_text = element.to_html()
    #escaped_text
    print(escaped_text)
    #horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your finding from Bard!")
    bot.send_message(message.chat.id, escaped_text, parse_mode="HTML")
    
# def fetch_horoscope(message, sign):
#     day = message.text
#     horoscope = get_daily_horoscope(sign, day)
#     data = horoscope["data"]
#     horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
#     bot.send_message(message.chat.id, "Here's your horoscope!")
#     bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


# In[ ]:


#bot.infinity_polling()
while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(5)
        continue


