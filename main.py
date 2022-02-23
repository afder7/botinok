import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup as bs
import random
import datetime
import re as regex
# msg epl table
# choose your favourite team
# msg their results


class botinok:

    def __init__(self, user_id):
        self.requests = ["любимая команда", "выбрать любимую команду", "результаты", "турнирная таблица", "список возможностей"]
        self.eplTeams = ["челси", "манчестер сити", "ливерпуль", "манчестер юнайтед", "вест хэм", "арсенал", "вулверхэмптон", "тоттенхэм", "брайтон", "саутгемптон", "лестер", "астон вилла", "кристал пэлас", "брентфорд", "лидс", "эвертон", "ньюкасл", "уотфорд", "бёрнли", "бернли", "норвич"]
        self.teamLinks = {"челси": "https://soccer365.ru/clubs/184/",
                         "манчестер сити": "https://soccer365.ru/clubs/90/",
                         "ливерпуль": "https://soccer365.ru/clubs/79/",
                         "манчестер юнайтед": "https://soccer365.ru/clubs/92/",
                         "вест хэм": "https://soccer365.ru/clubs/33/",
                         "арсенал": "https://soccer365.ru/clubs/2/",
                         "вулверхэмптон": "https://soccer365.ru/clubs/41/",
                         "тоттенхэм": "https://soccer365.ru/clubs/163/",
                         "брайтон": "https://soccer365.ru/clubs/265/",
                         "саутгемптон": "https://soccer365.ru/clubs/759/",
                         "лестер": "https://soccer365.ru/clubs/77/",
                         "астон вилла": "https://soccer365.ru/clubs/214/",
                         "кристал пэлас": "https://soccer365.ru/clubs/67/",
                         "брентфорд": "https://soccer365.ru/clubs/6997/",
                         "лидс": "https://soccer365.ru/clubs/6930/",
                         "эвертон": "https://soccer365.ru/clubs/191/",
                         "ньюкасл": "https://soccer365.ru/clubs/210/",
                         "уотфорд": "https://soccer365.ru/clubs/6978/",
                         "бёрнли": "https://soccer365.ru/clubs/6983/",
                         "бернли": "https://soccer365.ru/clubs/6983/",
                         "норвич": "https://soccer365.ru/clubs/227/"}
        self.uid = user_id
        self.name = self.userName(user_id)
        self.favTeam = "челси"

    def userName(self, user_id):
        link1 = f"https://vk.com/id{user_id}"
        page = bs(requests.get(link1).content, features="html.parser")
        re = page.find_all("title")[0]
        return re.text.replace("<", "").replace(">", "")

    def send(self, message):
        msg = message.lower()
        if msg not in self.requests:
            if msg in self.eplTeams:
                with open("activity_log.txt", "a") as f:
                    f.write(f"User {self.uid} has chosen new favourite team {msg} instead of {self.favTeam}\n")
                self.favTeam = msg
                return "Теперь это твоя новая любимая команда"
            return f'{random.choice(["Что-то на непонятном", "Я не понял...", "Ты это мне?", "Ты имел ввиду что-то другое?"])}. Чтобы узнать о возможностях бота напиши "список возможностей"'
        if msg == "выбрать любимую команду":
            re = "Выбери команду (писать строго так, как указано в списке ниже):"
            for i in self.eplTeams:
                re += f"\n{i.title()}"
            return re
        if msg == "турнирная таблица":
            link2 = "https://m.sports.ru/epl/table/"
            soup2 = bs(requests.get(link2).content, features="html.parser")
            results2 = [i.text for i in soup2.find_all("a") if i.text.lower() in self.eplTeams]
            re = f"Турнирная таблица АПЛ на {str(datetime.date.today()).replace('-', '.')}:"
            for i, x in enumerate(results2):
                re += f"\n{i + 1} - {x}"
            return re
        if msg == "результаты":
            link3 = self.teamLinks[self.favTeam]
            soup3 = bs(requests.get(link3).content, features="html.parser")
            results3 = soup3.find_all(class_="block_body_nopadding")[0].text.replace("\n", "").split("\xa0")
            de = "Прошедшие матчи:"
            re = "\nПредстоящие матчи:"
            cre, cde = 0, 0
            for i, x in enumerate(results3[:-1]):
                if cre == 3 and cde == 3:
                    break
                if "Премьер-Лига" in results3[i + 1] and "-" in x[x.find(","):] and cre < 3:
                    _ = regex.sub(r"(\w)([А-Я])", r"\1 \2", x[x.find(',') + 2:])
                    re += f"\n{x[x.find(',') - 5:x.find(',')]} {_}"
                    cre += 1
                elif "Премьер-Лига" in results3[i + 1] and "-" not in x[x.find(","):] and cde < 3:
                    _ = regex.sub(r"(\w)([А-Я])", r"\1 \2", x[x.find(',') + 2:])
                    de += f"\n{x[x.find(',') - 5:x.find(',')]} {_}"
                    cde += 1
            return de + re
        if msg == "любимая команда":
            return f"Сейчас твоя любимая команда - {self.favTeam.title()}"
        if msg == "список возможностей":
            return "Возможности ботинка (команда - действие):\n" \
                   "Ботинок рассылает результаты вашей любимой команды (об этом ниже) и уведомляет о будущих играх каждое утро.\n" \
                   "Выбрать любимую команду - Обновить/Задать вашу любимую команду АПЛ.\n" \
                   "Результаты - Получить последние результаты вашей любимой команды.\n" \
                   "Турнирная таблица - Вывести таблицу АПЛ.\n" \
                   "Любимая команда - Вывести вашу нынешнюю любимую команду.\n" \
                   "Пока что это всё, но в скором будущем я добавлю другие лиги и возможности... возможно."
        return f'{random.choice(["Что-то на непонятном", "Я не понял...", "Ты это мне?", "Ты имел ввиду что-то другое?"])}. Чтобы узнать о возможностях бота напиши "список возможностей"'


def write(user_id, message):
    with open("activity_log.txt", "a") as f:
        f.write(f'Answering to user {event.user_id}\n')
    session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


session = vk_api.VkApi(token="4e489932ddd7cfbf1b065f482f375eae7b8251913f4d596943bafb2cac079177a2ac83ce2ed9bc177f7b6")
longpoll = VkLongPoll(session)
users = dict()
sent = False
with open("activity_log.txt", "w", encoding="utf-8") as f:
    f.write("Bot starting...\n")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            with open("activity_log.txt", "a") as f:
               f.write(f'Received new message "{event.text}" from user {event.user_id}\n')
            if event.user_id not in users:
                users[event.user_id] = botinok(event.user_id)
            bot = users[event.user_id]
            write(event.user_id, users[event.user_id].send(event.text))
    if str(datetime.datetime.now().time()).split(":")[0:2] == ["09", "00"] and not sent:
        sent = True
        if event.user_id not in users:
            users[event.user_id] = botinok(event.user_id)
        bot = users[event.user_id]
        write(event.user_id, f"Доброе утро, {' '.join(bot.userName(event.user_id).split()[0:2])}! Результаты матчей команды {bot.favTeam}:\n{bot.send('результаты')}")
    if str(datetime.datetime.now().time()).split(":")[0:2] == ["00", "00"]:
        sent = False
