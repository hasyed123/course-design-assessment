# Used for holding state in the data layer
class CourseEntity:
    def __init__(self, id, name, students=None, assignments=None, submissions=None) -> None:
        self.id = id
        self.name = name
        self.students = students if students is not None else set()
        self.assignments = assignments if assignments is not None else dict()
        self.submissions = submissions if submissions is not None else dict()