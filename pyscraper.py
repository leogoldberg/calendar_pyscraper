import requests
import re
import parsers
from bs4 import BeautifulSoup
from csv import writer


response = requests.get('https://www.sfu.ca/students/calendar/2019/spring/courses/cmpt.html')

soup = BeautifulSoup(response.text, 'html.parser')

# get_text()


# finding sections:
courses = soup.find(attrs={"class": "sub-menu"}).contents
print(courses)
courses = course[:-2]
for cour
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


def time_convert(time):
    period = time[-2:]
    hour = re.search('\d+(?=:)', time)[0]
    minute = re.search('(?<=:)\d+', time)[0]
    if period == "AM":
        if int(hour) < 10:
            return "0"+hour+":"+minute
        else:
            return hour+":"+minute
    else:
        if int(hour) == 12:
            return hour+":"+minute
        hour = str(int(hour)+12)
        return hour+":"+minute


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


def write_csv(row, date_list):
    for day in date_list:
        csv_writer.writerow(row)

    # set up csv file
with open('room_info.csv', 'w') as csv_file:
    csv_writer = writer(csv_file)
    headers = ['Room', 'Day', 'Start Time', 'End Time', 'Course']
    csv_writer.writerow(headers)

    # main processing:
    if(len(room_check) < 7):
        room_times = room_times.contents[2].find_next_sibling()
        time_day = room_times.contents[0]
        room = room_times.contents[2]

        name = name_parser(name)
        info = room_parser(room, time_day)
        date_list = date_split(info[3])
        start_time = time_convert(info[1])
        end_time = time_convert(info[2])

        for day in date_list:
            row = [info[0], day, start_time, end_time, name]
            csv_writer.writerow(row)
        # print(name)
        # print(info)
        # print(date_list)
        # print(start_time)
        # print(end_time)

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
        start_time1 = time_convert(info1[1])
        end_time1 = time_convert(info1[2])
        start_time2 = time_convert(info2[1])
        end_time2 = time_convert(info2[2])
        for day in date_list1:
            row = [info1[0], day, start_time1, end_time1, name]
            csv_writer.writerow(row)
        for day in date_list2:
            row = [info2[0], day, start_time2, end_time2, name]
            csv_writer.writerow(row)
        # print(name)
        # print(info1)
        # print(info2)
        # print(date_list1)
        # print(date_list2)
        # print(start_time1)
        # print(end_time1)
        # print(start_time2)
        # print(end_time2)
