from DB.sqlite3_db import relational_database
from DB.mongo_db import mongo_db


class Student:
    def __init__(self, name, surname, age, gpa, student_id=None):
        self.student_id = student_id
        self.name = name
        self.surname = surname
        self.age = age
        self.gpa = gpa

    def __str__(self):
        return f'ID: {self.student_id}, Name: {self.name}, Surname: {self.surname}'

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.student_id == other.student_id
        return False

    def __repr__(self):
        return f"Student: {self.name} {self.surname} {self.age} years old"

    @classmethod
    def is_empty(cls, db_name):
        if db_name == "sqlite3":
            return relational_database.is_empty("Student")
        else:
            return mongo_db.is_empty("Student")

    @classmethod
    def get(cls, student_id, db_name):
        if db_name == "sqlite3":
            values = relational_database.get("Student", student_id)
        else:
            values = mongo_db.get("Student", student_id)

        if values is None:
            return None

        student = Student(values["name"], values["surname"], values["age"], values["gpa"], student_id)
        return student

    @classmethod
    def get_list(cls, db_name, **kwargs):
        if db_name == "sqlite3":
            result = relational_database.get_list("Student", **kwargs)
        else:
            result = mongo_db.get_list("Student", **kwargs)

        students = []
        for row in result:
            students.append(Student(row["name"], row["surname"], row["age"], row["gpa"]))
        return students

    def save(self, db_name):
        if db_name == "sqlite3":
            self.student_id = relational_database.save("Student", name=self.name,
                                                       surname=self.surname, age=self.age, gpa=self.gpa,
                                                       human_id=self.student_id)
        else:
            self.student_id = mongo_db.save("Student", name=self.name,
                                            surname=self.surname, age=self.age, gpa=self.gpa,
                                            human_id=self.student_id)

        return self
