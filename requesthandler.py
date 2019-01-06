import requests
from bs4 import BeautifulSoup

# returns list of courses offered by department in the spring term


def get_courses(department):
    response = requests.get(
        'https://www.sfu.ca/students/calendar/2019/spring/courses/'+department+'.html')

    soup = BeautifulSoup(response.text, 'html.parser')

    # finding courses:
    courses = soup.find(attrs={"class": "sub-menu"})
    # print(courses)
    # print(courses)
    courses_list = []
    courses = courses.find_all('option')
    courses = courses[1:]
    for course in courses:
        course = course.contents[0]
        courses_list.append(course)
        # print(course)
    return courses_list

# returns list of urls for various sections of a course


def get_sections(department, course_number):

    response = requests.get(
        'https://www.sfu.ca/students/calendar/2019/spring/courses/'+department+'/'+course_number+'.html')

    soup = BeautifulSoup(response.text, 'html.parser')
    sections_list = []
    sections = soup.find_all(attrs={"target": "_blank"})
    # course does not offer any sections in this term
    if sections == "None":
        return sections
    # course has some offerings in this term
    else:
        for section in sections:
            section = section['href']
            sections_list.append(section)
            # print(section)
        return sections_list
