from DB.sqlite3_db import relational_database
from DB.mongo_db import mongo_db


class Advisor:
    def __init__(self, name, surname, age, students=None, advisor_id=None,):
        self.advisor_id = advisor_id
        self.name = name
        self.surname = surname
        self.age = age
        self.students = students

    def __str__(self):
        return f'ID: {self.advisor_id}, Name: {self.name}, Surname: {self.surname}'

    def __eq__(self, other):
        if isinstance(other, Advisor):
            return self.advisor_id == other.advisor_id
        return False

    def __repr__(self):
        return f"Advisor: {self.name} {self.surname} {self.age} years old"

    @classmethod
    def is_empty(cls, db_name):
        if db_name == "sqlite3":
            return relational_database.is_empty("Advisor")
        else:
            return mongo_db.is_empty("Advisor")

    @classmethod
    def get(cls, advisor_id, db_name):
        if db_name == "sqlite3":
            values = relational_database.get("Advisor", advisor_id)
        else:
            values = mongo_db.get("Advisor", advisor_id)

        if values is None:
            return None

        advisor = Advisor(values["name"], values["surname"], values["age"], values["id"], values["students"])
        return advisor

    @classmethod
    def get_list(cls, db_name, **kwargs):
        if db_name == "sqlite3":
            result = relational_database.get_list("Advisor", **kwargs)
        else:
            result = mongo_db.get_list("Advisor", **kwargs)

        advisors = []
        for row in result:
            advisors.append(Advisor(row["name"], row["surname"], row["age"], row["students"]))
        return advisors

    def save(self, db_name):
        if db_name == "sqlite3":
            self.advisor_id = relational_database.save("Advisor", name=self.name, surname=self.surname, age=self.age,
                                                       human_id=self.advisor_id)
        else:
            self.advisor_id = mongo_db.save("Advisor", name=self.name, surname=self.surname, age=self.age,
                                            human_id=self.advisor_id, students=self.students)
        return self
