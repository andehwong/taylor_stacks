import requests
from bs4 import BeautifulSoup

from components import extractor, transformer


class Scraper:

    def __init__(self, url):
        self.web_page = requests.get(url)
        self.soup = BeautifulSoup(self.web_page.content, 'html.parser')

    def get_course_headers_list(self):
        # Retrieve all course headers from raw HTML
        course_headers_raw = extractor.get_all_specified_data(self.soup, 'h4', 'courseTitleNoBlueLink')

        # Convert raw course info string into CourseHeader objects
        course_headers_list = []
        for course_header_raw in course_headers_raw:
            course_headers_list.append(transformer.transform_to_course_header(course_header_raw))

        return course_headers_list

    def get_course_details_list(self):
        # Retrieve all panel bodies from raw HTML
        # Remove the first two elements since they are not courses
        panel_bodies = extractor.get_all_specified_data(self.soup, 'div', 'panel-body')[2:]
        panel_body_contents = []
        for panel_body in panel_bodies:
            panel_body_contents.append(extractor.get_all_specified_data(panel_body, 'div', 'col-xs-12'))

        # Convert each panel_body_data into a form of course details data
        course_details_list = []
        for panel_body_data in panel_body_contents:
            course_details_list.append(transformer.transform_to_course_details(panel_body_data))

        return course_details_list
