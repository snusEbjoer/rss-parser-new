import asyncio
import feedparser
from bs4 import BeautifulSoup
import requests
from dateutil import parser

class RssParser:
    def __init__(self): #self.parse_date(self.get_last_news()["pub_date"])
        self.last_post_date = self.parse_date("Sun, 28 Apr 2024 17:11:37 +0300")
        self.new_posts = []
    
    def extract_text(self,p): # достаём текст из <p> тэгов исключая кнопки и пустые тэги
        text = ""
        for el in p:
            text += el.get_text()
        return text

    def extract_img_src(self, img): # получаем ссылку на картинку
        return img[0]["src"]
    
    def parse_date(self, date_str): # парсим из строки в datetime 
        dt = parser.parse(date_str)
        return dt
    
    def compare_dates(self, date_str): # сравниваем даты
        return self.last_post_date < self.parse_date(date_str)
    
    def get_feed(self):
        response = requests.get("https://volgograd-trv.ru/rss.xml") # получаем gеt запросом html новостей 
        feed = feedparser.parse(response.text) # парсим текст
        return feed
    
    def get_last_news(self): # получаем последнюю новость
        feed = self.get_feed()
        news = dict()
        entry = feed.entries[0]

        content = entry["content"][0]["value"] 
        
        soup = BeautifulSoup(content, "html.parser")
        p = soup.find_all("p")
        img = soup.find_all("img")

        news["title"] = entry["title"]
        news["link"] = entry["link"]
        news["author"] = entry["author"]
        news["category"] = entry["category"]
        news["pub_date"] = entry["published"]
        news["content"] = self.extract_text(p)
        news["img"] = self.extract_img_src(img)

        return news

    def append_new_posts(self): # сравниваем даты предыдущей новости с текущей и если prev < curr то добавляем новость в массив
        news = self.get_last_news()
        if self.compare_dates(news["pub_date"]): # закоментировать строку нижу типо в волгограде есть новости
            self.last_post_date = self.parse_date(news["pub_date"])
            self.new_posts.append(news)

            
    
