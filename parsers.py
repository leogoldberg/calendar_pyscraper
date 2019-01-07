import re


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
    # something wrong with location, i.e TBA locatoin
    else:
        return "Bad Date String"


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
    print("the room is " + room)
    if room == "Location: TBA":
        return "None"

    room_info = re.search(
        '(.*)\s(((\d+|[A-Z]+)(?=,))|((\d+)(?=[A-Z])[A-Z]+(?=,))|((\d+)(?=\.)\.\d+(?=,))|((\d*[A-Z]*\d*[A-Z]*)(?=,)))', room)[0]
    time_start = re.search('\d+\:\d+\s[a-zA-Z]+', time_day)[0]
    time_end = re.search('(?<=– )(.*)', time_day)[0]  # match everything after pesky en dash!

    # matches if space followed by number follows string
    day = re.search('(.*)(?=\s\d+:\d+\s[A-Z]{2}\s–)', time_day)
    if day:
        return [room_info, time_start, time_end, day[0]]
    else:
        return "None"


def name_parser(name):
    return re.search('(?<=-\s)(.*)$', name)[0]  # match everything after '- '


def single_room_parser(room_times, name):
    room_times = room_times.contents[2].find_next_sibling()
    time_day = room_times.contents[0]
    print(room_times.contents[0])
    if room_times.contents[0] == "Location: TBA" or room_times.contents[0] == "Distance Education":
        return "None"
    room = room_times.contents[2]
    name = name_parser(name)
    info = room_parser(room, time_day)
    if info != "None":
        date_list = date_split(info[3])
        start_time = time_convert(info[1])
        end_time = time_convert(info[2])
        print(date_list)
    else:
        return "None"
    if date_list != "Bad Date String":
        return [name, info[0], start_time, end_time, date_list]
    else:
        return "None"


def double_room_parser(room_times, room_check, name):
    room_times1 = room_times.contents[2].find_next_sibling()
    time_day1 = room_times1.contents[0]
    room1 = room_times1.contents[2]

    if room_times1.contents[0] == "Location: TBA" or room_times1.contents[0] == "Distance Education":
        return "None"

    room_times2 = room_times.contents[4].find_next_sibling()
    time_day2 = room_times2.contents[0]
    room2 = room_times2.contents[2]

    if room_times2.contents[0] == "Location: TBA" or room_times2.contents[0] == "Distance Education":
        return "None"

    info1 = room_parser(room1, time_day1)
    info2 = room_parser(room2, time_day2)
    if info1 != "None" and info2 != "None":
        name = name_parser(name)
        date_list1 = date_split(info1[3])
        date_list2 = date_split(info2[3])
        start_time1 = time_convert(info1[1])
        end_time1 = time_convert(info1[2])
        start_time2 = time_convert(info2[1])
        end_time2 = time_convert(info2[2])
    else:
        return "None"
    if date_list1 != "Bad Date String" and date_list2 != "Bad Date String":
        return [name, info1[0], start_time1, end_time1, date_list1, info2[0], start_time2, end_time2, date_list2]
    else:
        return "None"
