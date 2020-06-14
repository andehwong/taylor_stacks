import json

from components import transformer
from components.scraper import Scraper
from models.response import Response


def main():
    url = 'https://www.westerncalendar.uwo.ca/Courses.cfm?Subject=COMPSCI&SelectedCalendar=Live'
    scraper = Scraper(url)
    course_headers = scraper.get_course_headers_list()
    course_details = scraper.get_course_details_list()

    response = Response(transformer.generate_course_summary_list(course_headers, course_details))
    json_response = json.dumps(vars(response), default=lambda x: x.__dict__, indent=4)
    print(json_response)


if __name__ == '__main__':
    main()
