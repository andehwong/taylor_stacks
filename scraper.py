import requests
import json
from bs4 import BeautifulSoup

from extractor import Extractor
from models.course_summary import CourseSummary
from models.response import Response
from transformer import Transformer


class Scraper:

    def __init__(self, url):
        self.url = url

    def initialize_soup_obj(self):
        web_page = requests.get(self.url)
        return BeautifulSoup(page.content, 'html.parser')


########## Scraper Testing Code ##########

# Initialize soup object with URL
URL = 'https://www.westerncalendar.uwo.ca/Courses.cfm?Subject=COMPSCI&SelectedCalendar=Live'
scraper = Scraper(URL)
page = requests.get(URL)
soup = scraper.initialize_soup_obj()

# Retrieve all course headers from raw HTML
course_headers_raw = Extractor.get_all_specified_data(soup, 'h4', 'courseTitleNoBlueLink')

# Convert raw course info string into CourseInfo objects
course_headers_list = []
for course_header_raw in course_headers_raw:
    course_headers_list.append(Transformer.transform_to_course_header(course_header_raw))

# Retrieve all panel bodies from raw HTML
# Remove the first two elements since they are not courses
panel_bodies = Extractor.get_all_specified_data(soup, 'div', 'panel-body')[2:]
panel_body_contents = []
for panel_body in panel_bodies:
    panel_body_contents.append(Extractor.get_all_specified_data(panel_body, 'div', 'col-xs-12'))

# Convert each panel_body_data into a form of course details data
course_details_list = []
for panel_body_data in panel_body_contents:
    course_details_list.append(Transformer.transform_to_course_details(panel_body_data))

course_summary_list = []
for index, course_header in enumerate(course_headers_list):
    course_summary = CourseSummary(course_header.course_dept, course_header.course_code,
                                   course_header.course_suffix, course_header.course_name, course_details_list[index])
    course_summary_list.append(course_summary)

response = Response(course_summary_list)
json_response = json.dumps(vars(response), default=lambda x: x.__dict__, indent=4)
print(json_response)
