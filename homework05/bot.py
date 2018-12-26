import requests
import config
import telebot
from bs4 import BeautifulSoup
from datetime import *
import datetime
import calendar


bot = telebot.TeleBot(config.access_token)

def week_now():
    now_week = datetime.date.today().isocalendar()[1]
    if now_week % 2 == 1:
        week = 2
    else:
        week = 1
    return week


def get_page(group, week=0):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, day_number):
    soup = BeautifulSoup(web_page, "html5lib")

     # Получаем таблицу с расписанием на указанный день
    schedule_table = soup.find("table", attrs={"id": day_number})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, week, group = message.text.split()
    day_number = ''
    if day == '/monday':
        day_number += '1day'
    if day == '/tuesday':
        day_number += '2day'
    if day == '/wednesday':
        day_number += '3day'
    if day == '/thursday':
        day_number += '4day'
    if day == '/friday':
        day_number += '5day'
    if day == '/saturday':
        day_number += '6day'
    if day == '/sunday':
        day_number += '7day'
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, day_number)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    date_now = str(date.today().isoweekday())
    day_number = date_now + 'day'
    web_page = get_page(group, week_now())
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, day_number)
    now = datetime.datetime.now()
    now = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
    resp = ''

    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        if datetime.strptime(time.split('-')[0], "%H:%M") > now:
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        else:
            if date.today().isoweekday() == 7:
                now_week = datetime.date.today().isocalendar()[1]
                if now_week % 2 == 1:
                    week = 1
                else:
                    week = 2
                day_number = '1day'
                web_page = get_page(group, week)
                times, locations, lessons = \
                    parse_schedule_for_a_day(web_page, day_number)
                resp += '<b>{}</b>, {}, {}\n'.format(times[0], locations[0], lessons[0])
            else:
                date_now = str(date.today().isoweekday() + 1)
                day_number = date_now + 'day'
                web_page = get_page(group, week_now())
                times, locations, lessons = \
                    parse_schedule_for_a_day(web_page, day_number)
                resp += '<b>{}</b>, {}, {}\n'.format(times[0], locations[0], lessons[0])
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    date_now = date.today().isoweekday()
    day_number = str(date_now) + 'day'
    if date_now == 7:
        date_now = '1'
        day_number = date_now + 'day'
        now_week = datetime.date.today().isocalendar()[1]
        if now_week % 2 == 1:
            week = 1
        else:
            week = 2
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, day_number)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, week, group = message.text.split()
    web_page = get_page(group, week)
    day_number = 1
    while day_number <= 7:
        times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, str(day_number))
        resp = ''
        req = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            day = calendar.day_name[day_number-1]
            resp += day + '\n' + '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        req += resp
        day_number += 1
    bot.send_message(message.chat.id, req, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)

