from bs4 import BeautifulSoup
import requests
from progress.bar import IncrementalBar
import os.path
import argparse

parser = argparse.ArgumentParser(description='Этот парсер предназначен для скачивания видео с сайта jut.su. \
    Чтобы начать парсить нужно запустить скрипт передав в аргумент --site ссылку на страницу где находится список серий.')
parser.add_argument("--hd", type=str, default="480p", help="Установка качества видео. По умолчанию 480p. Можно изменять на 360p, 720p, 1080p.")
parser.add_argument("--first", type=int, default=1, help="Установка серии с которой начинать скачивание. По умолчанию 1. Можно задать номер любой серии.")
parser.add_argument("--site", type=str, default='', help="Ссылка на страницу.")
args = parser.parse_args()
hd = args.hd
first = args.first
site = args.site

i = 0

headers = {
  'accept':'*/*',
  'accept-encoding':'identity;q=1, *;q=0',
  'accept-language':'ru-BY,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
  'cache-control':'no-cache',
  'dnt': '1',
  'pragma': 'no-cache',
  'sec-fetch-mode': 'no-cors',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-dest': 'video',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
  }

if (site != ''):
    req = requests.get(site, headers=headers)
    if (req.status_code == 200):
        soup = BeautifulSoup(req.text, 'html.parser')
        group = soup.find('div', {'class' : 'watch_l'})
        
        name = str(group.find('h1', {'class' : 'anime_padding_for_title'}).text).replace("Смотреть ", "").replace(' все серии и сезоны', '').replace(' все серии', '').replace(' ', '_')
        
        folder = name
        
        if not os.path.exists("in\\" + folder): os.makedirs("in\\" + name)
        
        max = len(group.find_all('a', {'class' : 'video'}))
        
        if (max >= first):  
            bar = IncrementalBar('Countdown', max = max)
            for href in group.find_all('a', {'class' : 'video'}):
                bar.next()
                i = i + 1
                if i >= first:
                    site = 'https://jut.su' + href['href']
                    req = requests.get(site, headers=headers)
                    soup = BeautifulSoup(req.text, 'html.parser')
                    video_href = soup.find('source', {'label' : hd})
                    p = requests.get(video_href['src'], headers=headers)
                    if href.text[-5:] == "фильм":
                        name = name + "_фильм"

                    if p.status_code != 200:
                        print("Ошибка " + str(p.status_code) + " при скачивании фала " + video_href['src'])
                    else:        
                        out = open("in\\" + folder + "\\" + str(i) + "_" + name + ".mp4", "wb")
                        out.write(p.content)
                        out.close()

        else:
            print("Ошибка! Аргумент --first больше количества серий. Запустите программу с аргументом -h")
    else:
        print("Ошибка доступа к сайту: " + str(req.status_code))
else:
    print("Ошибка! Не введен аргумент --site. Запустите программу с аргументом -h")

print("Программа завершена")
