import re
from models.course import Course
from models.course_detail import CourseDetails
from models.course_header import CourseHeader
from models.course_summary import CourseSummary
from models.pre_reqs import PreRequisites
from models.anti_reqs import AntiRequisites


def generate_course_summary_list(course_headers_list, course_details_list):
    course_summary_list = []
    for index, course_header in enumerate(course_headers_list):
        course_summary = CourseSummary(course_header.course_dept, course_header.course_code,
                                       course_header.course_suffix, course_header.course_name,
                                       course_details_list[index])
        course_summary_list.append(course_summary)

    return course_summary_list


def transform_to_course_header(header_string):
    split_course_string = re.split(r'\s+(?=\d)|(?<=\d)\s+', header_string.text, 0)
    course_dept = split_course_string[0]

    split_course_string = split_course_string[1].split(' ', 1)
    course_code = re.sub("[^0-9]", "", split_course_string[0])
    course_suffix = re.sub("[^A-Z/]", "", split_course_string[0])
    course_name = split_course_string[1].strip()

    current_course_header = CourseHeader(course_code, course_name, course_suffix, course_dept)
    return current_course_header


def transform_to_course_details(panel_body_data):
    course_details = CourseDetails()

    for index, panel_body_detail in enumerate(panel_body_data):
        # First item is always the description, so handle that first
        if index == 0:
            setattr(course_details, 'description', panel_body_detail.text.strip())
            continue

        # Read the "key" of the panel-body to determine how to process the string data
        key_value_for_panel_body = panel_body_detail.text.strip().split(": ", 1)
        if key_value_for_panel_body[0] == "Antirequisite(s)":
            setattr(course_details, 'anti_reqs',
                    transform_to_anti_req_obj(key_value_for_panel_body[1][:-1]))
        elif key_value_for_panel_body[0] == "Prerequisite(s)":
            setattr(course_details, 'pre_reqs',
                    transform_to_pre_req_obj(key_value_for_panel_body[1].rstrip('.')))
            # elif key_value_for_panel_body[0] == "Corequisite(s)":
            #     Transformer.transform_to_pre_req_obj(key_value_for_panel_body[1])
        elif key_value_for_panel_body[0] == "Extra Information":
            setattr(course_details, 'additional_info',
                    key_value_for_panel_body[1].split('.')[0])
        elif key_value_for_panel_body[0] == "Course Weight":
            setattr(course_details, 'course_weight',
                    float(re.search(': (.+?)\n', panel_body_detail.text.strip()).group(1)))

    return course_details


def transform_to_anti_req_obj(anti_req_string):
    anti_req_obj = AntiRequisites()

    # Split the string on various delimiters
    # Replace is to replace any 'and' joiners at the end of lists
    split_anti_req_string = re.split(r', and |, the former |, ', anti_req_string.replace('B and ', ', '))

    anti_req_course_list = []
    for course_name in split_anti_req_string:

        # If the course_name has more than one course joined by 'or'
        if 'B or ' in course_name:
            list_of_or_courses = []
            for course in course_name.split(' or '):
                course_dept_and_code = course.rsplit(' ', 1)
                temp_course = Course(course_dept_and_code[0], re.sub("[^0-9]", "", course_dept_and_code[1]),
                                     re.sub("[^A-Z/]", "", course_dept_and_code[1]))
                list_of_or_courses.append(temp_course)
            setattr(anti_req_obj, 'one_of', list_of_or_courses)

        # If course_name contains an anti-req taken during a specific session (Fall/Winter, Summer, etc.)
        elif 'if taken during' in course_name:
            course_name_list = course_name.split(' if taken during ')
            course_dept_and_code = course_name_list[0].rsplit(' ', 1)
            temp_course = Course(course_dept_and_code[0], re.sub("[^0-9]", "", course_dept_and_code[1]),
                                 re.sub("[^A-Z/]", "", course_dept_and_code[1]))
            school_session = course_name_list[1].replace('the ', '')

            # If the course_name contains the phrase 'academic year', that means full year
            if 'academic year' in course_name_list[1]:
                year_anti_req_map = {
                    'term': 'Year',
                    'years': school_session.split(' ', 1)[0].split('-')
                }
                setattr(temp_course, 'if_taken_in', year_anti_req_map)
            # Else, all other instances can be processed into session and years
            else:
                year_anti_req_map = {
                    'term': school_session.split(' ', 1)[0],
                    'years': school_session.split(' ', 1)[1].replace(' or ', ',').split(' ')[0].split(',')
                }
                setattr(temp_course, 'if_taken_in', year_anti_req_map)

            # Append the course object to the anti-req course list
            anti_req_course_list.append(temp_course)

        # No special handling, split into course dept and course code and create Course obj
        else:
            course_dept_and_code = course_name.rsplit(' ', 1)
            temp_course = Course(course_dept_and_code[0], re.sub("[^0-9]", "", course_dept_and_code[1]),
                                 re.sub("[^A-Z/]", "", course_dept_and_code[1]))
            anti_req_course_list.append(temp_course)

    anti_req_obj.course_list = anti_req_course_list
    return anti_req_obj


"""
TODO:
1. (DONE) Basic course list (no either, or, "1.0 Course in", etc.)
2. 'Or' pre-reqs (one of the following)
3. Either
4. 1.0/2.0/etc. Courses in
5. Minimum mark in
"""


def transform_to_pre_req_obj(pre_req_string):
    pre_req_obj = PreRequisites()

    pre_req_course_list = []
    if "Either" in pre_req_string:
        pass
    elif "or" in pre_req_string:
        pass
    elif "course" in pre_req_string:
        pass
    else:
        # Since recommended courses are not required, we will ignore them and create the pre-req list
        pre_req_string_remove_recs = pre_req_string.split(';')[0]
        pre_req_list = re.split(r' and |, ', pre_req_string_remove_recs)

        for course_name in pre_req_list:
            course_dept_and_code = course_name.rsplit(' ', 1)
            temp_course = Course(course_dept_and_code[0], re.sub("[^0-9]", "", course_dept_and_code[1]),
                                 re.sub("[^A-Z/]", "", course_dept_and_code[1]))
            pre_req_course_list.append(temp_course)

    pre_req_obj.course_list = pre_req_course_list
    return pre_req_obj
