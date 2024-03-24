import json
from Models.advisor import Advisor
from Models.student import Student
from Models.studentAdvisor import StudentAdvisor
from DB.sqlite3_db import relational_database


class MainClass:
    s = "sqlite3"  # name for sqlite
    m = "mongodb"  # name for mongodb

    @classmethod
    def fill_relational_db(cls, info):
        for advisor_data in info["advisors"]:
            advisor = Advisor(advisor_data['name'], advisor_data['surname'], advisor_data['age'])
            advisor.save(cls.s)
            for student_data in advisor_data['students']:
                student = Student(student_data['name'], student_data['surname'], student_data['age'],
                                  student_data['gpa'])
                student.save(cls.s)

                student_advisor = StudentAdvisor(advisor.advisor_id, student.student_id)
                student_advisor.save()

    @classmethod
    def fill_mongo_db(cls, info):
        for advisor_data in info["advisors"]:
            advisor = Advisor(advisor_data['name'], advisor_data['surname'],
                              advisor_data['age'], advisor_data['students'])
            advisor.save(cls.m)
            for student_data in advisor_data['students']:
                student = Student(student_data['name'], student_data['surname'], student_data['age'],
                                  student_data['gpa'])
                student.save(cls.m)

    @classmethod
    def main(cls):
        relational_database.create_db()

        if Advisor.is_empty(cls.s) or StudentAdvisor.is_empty() or Student.is_empty(cls.s):
            with open('Data/data.json', 'r') as file:
                data = json.load(file)
            cls.fill_relational_db(data)

        if Advisor.is_empty(cls.m) or Student.is_empty(cls.m):
            with open('Data/data.json', 'r') as file:
                data = json.load(file)
            cls.fill_mongo_db(data)

        student = Student("Natia", "Pruidze", 22, "3.5")
        advisor = Advisor("Wolfgang", "Paul", 73,
                          [{
                              "name": "John",
                              "surname": "Doe",
                              "age": 20,
                              "gpa": 3.5
                          },
                              {
                                  "name": "Michael",
                                  "surname": "Johnson",
                                  "age": 19,
                                  "gpa": 3.2
                              }])
        student.save(cls.m)
        advisor.save(cls.m)
        student.save(cls.s)
        advisor.save(cls.s)

        print(Student.get(32, cls.s))
        print(Student.get_list(cls.m, name=student.name, surname=student.surname))
        print(Advisor.get_list(cls.m, name=advisor.name, surname=advisor.surname))


if __name__ == '__main__':
    MainClass.main()
