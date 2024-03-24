import sqlite3


class RelationalDbManager:
    def __init__(self):
        self.conn = sqlite3.connect('DB/university.db')
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.c = self.conn.cursor()

    def create_db(self):
        self.c.execute("""
                    CREATE TABLE IF NOT EXISTS Student(
                        student_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name TEXT NOT NULL,
                        surname TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        gpa REAL NOT NULL
                    )""")

        self.c.execute("""
                    CREATE TABLE IF NOT EXISTS Advisor(
                        advisor_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name TEXT NOT NULL,
                        surname TEXT NOT NULL,
                        age INTEGER NOT NULL
                    )""")

        self.c.execute("""
                    CREATE TABLE IF NOT EXISTS StudentAdvisor(
                        advisor_id INTEGER NOT NULL,
                        student_id INTEGER NOT NULL,
                        PRIMARY KEY(student_id, advisor_id),
                        FOREIGN KEY (student_id) REFERENCES Student(student_id),
                        FOREIGN KEY (advisor_id) REFERENCES Advisor(advisor_id)
                    )""")
        self.conn.commit()

    def is_empty(self, table_name):
        query = "SELECT COUNT(*) FROM {}".format(table_name)
        return self.c.execute(query).fetchone()[0] == 0

    def get(self, table_name, human_id):
        if table_name == "Student":
            result = self.c.execute("SELECT * FROM Student WHERE student_id=?", (human_id,))
        else:
            result = self.c.execute("SELECT * FROM Advisor WHERE advisor_id=?", (human_id,))

        values = result.fetchall()
        if not values:
            return None
        return values[0]

    def get_list(self, table_name, **kwargs):
        if table_name == "Student":
            query = "SELECT DISTINCT * FROM Student WHERE "
        else:
            query = "SELECT DISTINCT * FROM Advisor WHERE "

        conditions = []
        values = []
        for key, value in kwargs.items():
            conditions.append(f"{key} = ?")
            values.append(value)
        query += " AND ".join(conditions)
        result = self.c.execute(query, tuple(values))
        return list(result)

    def update(self, table_name, **kwargs):
        if table_name == "Student":
            self.c.execute("UPDATE Student SET name = ?, surname = ?, age = ?, gpa = ? WHERE Student.student_id = ?",
                           (kwargs["name"], kwargs["surname"], kwargs["age"], kwargs["gpa"], kwargs["human_id"]))
        else:
            self.c.execute("UPDATE Advisor SET name = ?, surname = ?, age = ? WHERE advisor_id = ?",
                           (kwargs["name"], kwargs["surname"], kwargs["age"], kwargs["human_id"]))

        self.conn.commit()

    def create(self, table_name, **kwargs):
        if table_name == "Student":
            self.c.execute("INSERT INTO Student (name, surname, age, gpa) VALUES (?, ?, ?, ?)",
                           (kwargs["name"], kwargs["surname"], kwargs["age"], kwargs["gpa"]))
        else:
            self.c.execute("INSERT INTO Advisor (name, surname, age) VALUES (?, ?, ?)",
                           (kwargs["name"], kwargs["surname"], kwargs["age"]))

        self.conn.commit()
        return self.c.lastrowid

    def save(self, table_name, **kwargs):
        human_id = None
        if table_name == "Student":
            human = self.c.execute("""
                            SELECT student_id 
                            from Student 
                            where name == ? and surname = ? and age = ? and gpa = ?""",
                                   (kwargs["name"], kwargs["surname"], kwargs["age"], kwargs["gpa"])).fetchone()

            if human is not None:
                human_id = human["student_id"]
        else:
            human = self.c.execute("""
                                        SELECT advisor_id 
                                        from Advisor 
                                        where name == ? and surname = ? and age = ?""",
                                   (kwargs["name"], kwargs["surname"], kwargs["age"])).fetchone()

            if human is not None:
                human_id = human["advisor_id"]

        if human_id is not None:
            self.update(table_name, **kwargs)
        else:
            human_id = self.create(table_name, **kwargs)

        return human_id

    def save_student_advisor(self, **kwargs):
        self.c.execute("INSERT INTO StudentAdvisor (advisor_id, student_id) VALUES (?, ?)",
                       (kwargs["advisor_id"], kwargs["student_id"]))
        self.conn.commit()

    def advisors_with_number_of_students(self):
        result = self.c.execute("""
        SELECT a.advisor_id, a.name, COUNT(s.student_id) AS number_of_students 
        FROM Student s INNER JOIN StudentAdvisor sa on sa.student_id = s.student_id
        INNER JOIN Advisor a ON sa.advisor_id = a.advisor_id
        GROUP BY a.advisor_id
        ORDER BY number_of_students
        """)

        print("Advisor ID\t\tName\t\t\tNumber of Students")
        print("-----------------------------------------------")
        for row in result.fetchall():
            print(f"{row['advisor_id']:<12}\t{row['name']:<20}\t{row['number_of_students']}")

    def students_with_number_of_advisors(self):
        result = self.c.execute("""
        SELECT s.student_id, s.name, COUNT(a.advisor_id) AS number_of_advisors
        FROM Student s INNER JOIN StudentAdvisor sa on sa.student_id = s.student_id
        INNER JOIN Advisor a ON sa.advisor_id = a.advisor_id
        GROUP BY s.student_id
        ORDER BY number_of_advisors
        """)

        print("\nStudent ID\t\tName\t\t\tNumber of Advisors")
        print("-----------------------------------------")
        for row in result.fetchall():
            print(f"{row['student_id']:<12}\t{row['name']:<20}\t{row['number_of_advisors']}")


relational_database = RelationalDbManager()
