from DB.sqlite3_db import RelationalDbManager, relational_database


class StudentAdvisor:
    def __init__(self, advisor_id, student_id):
        self.advisor_id = advisor_id
        self.student_id = student_id

    def __str__(self):
        return f'Advisor: {self.advisor_id}, Student: {self.student_id}'

    def __eq__(self, other):
        if isinstance(other, StudentAdvisor):
            return (self.advisor_id == other.advisor_id
                    and self.student_id == other.student_id)
        return False

    def __repr__(self):
        return f"Advisor: {self.advisor_id}, Student: {self.student_id}"

    @classmethod
    def is_empty(cls):
        return RelationalDbManager.is_empty(relational_database, "Student")

    def save(self):
        RelationalDbManager.save_student_advisor(relational_database,
                                                 advisor_id=self.advisor_id, student_id=self.student_id)
