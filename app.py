# pip install bardapi
#!pip install telegram-text
# !pip install pyTelegramBotAPI

import os
import telebot
from telegram_text import PlainText
from telebot import types
import requests
from bardapi import Bard

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TRANSLATE = "I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. "
COMEDIAN = "I want you to act as a stand-up comedian. I will provide you with some topics related to current events and you will use your wit, creativity, and observational skills to create a routine based on those topics. You should also be sure to incorporate personal anecdotes or experiences into the routine in order to make it more relatable and engaging for the audience. "
INTERVIEW = "I want you to act as an interviewer. I will be the candidate and you will ask me the interview questions for the position. I want you to reply as the interviewer and interviewee. Write all the conservation at once. I want you to only do the interview with me. Ask me the questions and give me my answers. Provide up to 15 questions. The position that I will be interviewing is:  "
bot = telebot.TeleBot(BOT_TOKEN)


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
    bard = Bard(session=session, timeout=30)
    bard.get_answer("What is my last prompt??")["content"]
    return str(bard.get_answer(message)["content"])


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton("Translation")
    itembtn2 = types.KeyboardButton("Stand-up Comedian")
    itembtn3 = types.KeyboardButton("Sample Interview QnA")
    itembtn4 = types.KeyboardButton("Normal Bard")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    sent_msg = bot.send_message(
        message.chat.id,
        "Choose which services of Bard you want to use:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(sent_msg, options)


def options(message):
    print(message.text)
    if message.text == "Translation":
        print("translate")
        sent_msg = bot.send_message(
            message.chat.id,
            "Please type in what you want to translate to English:",
            parse_mode="Markdown",
        )
        bot.register_next_step_handler(sent_msg, processor, mode="translate")

    elif message.text == "Stand-up Comedian":
        print("Stand-up Comedian")
        sent_msg = bot.send_message(
            message.chat.id,
            "Please type in the type of humor you like:",
            parse_mode="Markdown",
        )
        bot.register_next_step_handler(sent_msg, processor, mode="funny")
    elif message.text == "Sample Interview QnA":
        print("Interview QnA")
        sent_msg = bot.send_message(
            message.chat.id,
            "Please type in the position you wish to interview for:",
            parse_mode="Markdown",
        )
        bot.register_next_step_handler(sent_msg, processor, mode="interview")
    else:
        print("Normal Bard")
        sent_msg = bot.send_message(
            message.chat.id,
            "I’m Bard, your creative and helpful collaborator. I have limitations and won’t always get it right. Enter your prompt here: ",
            parse_mode="Markdown",
        )
        bot.register_next_step_handler(sent_msg, processor, mode="normal")


@bot.message_handler(commands=["Bard"])
def day_handler(message):
    text = "Please type the topic on what you want to know."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, processor)


def processor(message, mode):
    if mode == "translate":
        day = TRANSLATE + message.text
    elif mode == "funny":
        day = COMEDIAN + message.text
    elif mode == "interview":
        day = INTERVIEW + message.text
    else:
        day = message.text
    bardmsg = bard_api(day)
    data = bardmsg

    element = PlainText(data)
    escaped_text = element.to_html()
    print(escaped_text)
    bot.send_message(message.chat.id, "Here's your finding from Bard!")
    if len(escaped_text) > 4095:
        for x in range(0, len(escaped_text), 4095):
            parse_message(message, text=escaped_text[x : x + 4095])
            # bot.send_message(
            #     message.chat.id, text=escaped_text[x : x + 4095], parse_mode="HTML"
            # )
    else:
        # bot.send_message(message.chat.id, escaped_text, parse_mode="HTML")
        parse_message(message, escaped_text)


def parse_message(message, escaped_text):
    try:
        bot.send_message(message.chat.id, escaped_text, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, escaped_text, parse_mode="HTML")


bot.infinity_polling()
