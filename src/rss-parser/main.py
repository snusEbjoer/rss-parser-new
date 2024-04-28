import time
from bs4 import BeautifulSoup
from dateutil import parser
import requests
from classes.rss_parser import RssParser
from classes.db import Database
import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
import os

load_dotenv()
rss = RssParser()
db = Database()
bot = AsyncTeleBot(os.getenv("TG_KEY"))

def cut_msg(news): # обрезаем новость из-за лимита в 1024 символа на описание картинки
    msg = ""
    for k in news:
        if k == "category":
            msg += "#"+news[k]+"\n"
        else:
            msg += news[k]+"\n"
    if len(msg) > 1023:
        return msg[0:1023]
    return msg
  
async def send_news_to_all_subscribers(news): # отправляем всем подписчикам сообщение с новостью
   print("start sending")
   chat_ids = db.get_all_chats()
   img = requests.get(news["img"]).content
   
   for chat_id in chat_ids:
      await bot.send_photo(chat_id[0], img, caption=f"{cut_msg(news)}")

async def handle_rss_updates(): # "слушаем" рсс ленту на наличие новых постов
    while True:
        rss.append_new_posts()
        print("started", rss.new_posts)
        if len(rss.new_posts) >= 1:
            news = rss.new_posts.pop()
            news2 = news.copy()
            del news2["img"]
            db.create_news(*[news[k] for k in news2]) # ад...
            await send_news_to_all_subscribers(news)
        await asyncio.sleep(10)


@bot.message_handler(commands=['start'])
async def send_welcome(message): # хэндлим /start
    text = 'Теперь вы подписаны на новости Волгограда'
    db.add_chat(message.chat.id)
    print("sub")
    await bot.reply_to(message, text)


ioloop = asyncio.new_event_loop() # создаём эвент луп
ioloop.create_task(bot.polling()) # добавляем таски
ioloop.create_task(handle_rss_updates())
ioloop.run_forever() # запускаем