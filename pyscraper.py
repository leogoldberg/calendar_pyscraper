import requests
import requesthandler as rh
import re
import parsers as p
from bs4 import BeautifulSoup
from csv import writer


with open('room_info.csv', 'w') as csv_file:
    department = "cmpt"
    # set up csv file headers
    csv_writer = writer(csv_file)
    headers = ['Room', 'Day', 'Start Time', 'End Time', 'Course']
    csv_writer.writerow(headers)

    courses_list = rh.get_courses(department)
    print(courses_list)
    for course in courses_list:
        # print(course)
        course_number = re.search('(?<=\s)(.*)', course)[0]
        links = rh.get_sections(department, course_number)
        print(links)
        if links != "None":
            for link in links:
                print(link)
                response = requests.get(link)

                soup = BeautifulSoup(response.text, 'html.parser')
                name = soup.find(attrs={"id": "name"}).get_text()
                room_times = soup.find(class_='course-times')
                room_check = room_times.contents

                # parsing page data and writing to csv

                if(len(room_check) < 7):
                    data = p.single_room_parser(room_times, name)

                    if data != "None":
                        for day in data[4]:
                            row = [data[1], day, data[2], data[3], data[0]]
                            print(row)
                            csv_writer.writerow(row)
                        # print(name)
                        # print(info)
                        # print(date_list)
                        # print(start_time)
                        # print(end_time)

                else:
                    data = p.double_room_parser(room_times, room_check, name)
                    for day in data[4]:
                        row = [data[1], day, data[2], data[3], data[0]]
                        print(row)
                        csv_writer.writerow(row)
                    for day in data[8]:
                        row = [data[5], day, data[6], data[7], data[0]]
                        print(row)
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
