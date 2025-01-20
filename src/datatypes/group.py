from src.schemes.group_response import GroupResponse


class Group:
    def __init__(self):
        self.name = ""
        self.course = 0
        self.sub_group = 0
        self.spec = ""
        self.school_year = 0
        self.lessons = []

    def to_scheme(self):
        return GroupResponse(name=self.name, course=self.course, spec=self.spec, sub_group=self.sub_group,
                             school_year=self.school_year, lessons=[lesson.serialize() for lesson in self.lessons])

    def serialize(self):
        return GroupResponse(name=self.name, course=self.course, spec=self.spec, sub_group=self.sub_group,
                             school_year=self.school_year, lessons=[lesson.serialize() for lesson in self.lessons])

    def to_dict(self):
        serialized = {
            "name": self.name,
            "course": self.course,
            "sub_group": self.sub_group,
            "spec": self.spec,
            "school_year": self.school_year,
            "lessons": [lesson.to_dict() for lesson in self.lessons]
        }
        return serialized
