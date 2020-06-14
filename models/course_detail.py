class CourseDetails:

    def __init__(self, description='', anti_reqs=None, pre_reqs=None, additional_info='', course_weight=0):
        self.description = description
        self.anti_reqs = anti_reqs
        self.pre_reqs = pre_reqs
        self.additional_info = additional_info
        self.course_weight = course_weight
