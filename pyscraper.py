import requests
import requesthandler as rh
import re
import parsers as p
from bs4 import BeautifulSoup
from csv import writer


with open('room_info.csv', 'w') as csv_file:
    department_links = rh.get_departments()
    bad_links = ['http://www.sfu.ca/outlines.html?2019/spring/bus/726/g100']
    # set up csv file headers
    csv_writer = writer(csv_file)
    headers = ['Room', 'Day', 'Start Time', 'End Time', 'Course', 'Link']
    csv_writer.writerow(headers)

    for department in department_links:
        department_name = re.search('(?<=courses/)(.*)(?=.html)', department)[0]
        print(department_name)
        courses_list = rh.get_courses(department)
        print(courses_list)
        for course in courses_list:
            # print(course)
            course_number = re.search('(?<=\s)(.*)', course)[0]
            links = rh.get_sections(department_name, course_number)
            print(links)
            if links != "None":
                for link in links:
                    if link not in bad_links:
                        print(link)
                        response = requests.get(link, timeout=15)

                        soup = BeautifulSoup(response.text, 'html.parser')
                        name = soup.find(attrs={"id": "name"}).get_text()
                        room_times = soup.find(class_='course-times')
                        if room_times:  # non empty room time information
                            room_check = room_times.contents

                            # parsing page data and writing to csv

                            if(len(room_check) < 7):
                                data = p.single_room_parser(room_times, name)

                                if data != "None":
                                    for day in data[4]:
                                        row = [data[1], day, data[2], data[3], data[0], link]
                                        print(row)
                                        csv_writer.writerow(row)
                                    # print(name)
                                    # print(info)
                                    # print(date_list)
                                    # print(start_time)
                                    # print(end_time)

                            else:
                                data = p.double_room_parser(room_times, room_check, name)
                                if data != "None":
                                    for day in data[4]:
                                        row = [data[1], day, data[2], data[3], data[0], link]
                                        print(row)
                                        csv_writer.writerow(row)
                                    for day in data[8]:
                                        row = [data[5], day, data[6], data[7], data[0], link]
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
