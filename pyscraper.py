import requests
import re
from bs4 import BeautifulSoup
from csv import writer
from datetime import *

response = requests.get('http://www.sfu.ca/outlines.html?2019/spring/cmpt/295/d100')

soup = BeautifulSoup(response.text, 'html.parser')
# get_text()

# html parsing
name = soup.find(attrs={"id": "name"}).get_text()
room_times = soup.find(class_='course-times')
room_check = room_times.contents

# print(room_check)


def date_split(date):
    date_list = []
    date_len = len(date)
    if date_len == 6:
        date_list = [date[0:2], date[4:6]]
        return date_list
    elif date_len == 10:
        date_list = [date[0:2], date[4:6], date[8:10]]
        return date_list
    elif date_len == 2:
        date_list = [date]
        return date_list
    else:
        print("Ill formated date string")


def room_parser(room, time_day):
    # anything followed by space followed by one or more digits
    room_info = re.search('(.*)\s\d+', room)[0]
    time_start = re.search('\d+\:\d+\s[a-zA-Z]+', time_day)[0]
    time_end = re.search('(?<=– )(.*)', time_day)[0]  # match everything after pesky en dash!

    # matches if space followed by number follows string
    day = re.search('(.*)(?=\s\d+:\d+\s[A-Z]{2}\s–)', time_day)[0]

    return [room_info, time_start, time_end, day]


def name_parser(name):
    return re.search('(?<=-\s)(.*)$', name)[0]  # match everything after '- '


# main processing:
if(len(room_check) < 7):
    room_times = room_times.contents[2].find_next_sibling()
    time_day = room_times.contents[0]
    room = room_times.contents[2]

    name = name_parser(name)
    info = room_parser(room, time_day)
    date_list = date_split(info[3])
    print(name)
    print(info)
    print(date_list)

else:
    room_times1 = room_times.contents[2].find_next_sibling()
    time_day1 = room_times1.contents[0]
    room1 = room_times1.contents[2]

    room_times2 = room_times.contents[4].find_next_sibling()
    time_day2 = room_times2.contents[0]
    room2 = room_times2.contents[2]

    name = name_parser(name)
    info1 = room_parser(room1, time_day1)
    info2 = room_parser(room2, time_day2)
    date_list1 = date_split(info1[3])
    date_list2 = date_split(info2[3])
    print(name)
    print(info1)
    print(info2)
    print(date_list1)
    print(date_list2)
