# University Database Management System

This project is a Python-based application that manages student and advisor data in both a relational (SQLite3) and a NoSQL (MongoDB) database. It provides functionality to create, read, update, and delete (CRUD) student and advisor records, as well as establish relationships between students and advisors. The application is designed to demonstrate the implementation of database management systems using both relational and NoSQL approaches.

## Features

- **Create and manage student records**: The application allows you to create new student records by providing details such as name, surname, age, and GPA. Existing student records can be updated or deleted as needed.

- **Create and manage advisor records**: Similar to student records, you can create, update, and delete advisor records with details like name, surname, and age.

- **Store data in SQLite3 and MongoDB databases**: The application uses two different databases to store data: a relational SQLite3 database and a NoSQL MongoDB database. This allows for a comparison between the two approaches and demonstrates how to work with different database technologies.

- **Establish relationships between students and advisors**: The application supports the creation of relationships between students and advisors. Each student can be assigned one or more advisors, and each advisor can have multiple students.

- **Retrieve student and advisor data**: You can retrieve student and advisor data based on various criteria such as name, surname, age, or GPA (for students). The application provides methods to fetch individual records or lists of records matching specific conditions.

- **Generate reports**: The application includes functionality to generate reports on the number of students per advisor and the number of advisors per student. These reports provide insights into the relationships between students and advisors.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/natia02/Sqlite3MongoDB.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

The required packages include `sqlite3` for working with the SQLite3 database and `pymongo` for interacting with the MongoDB database.

## Usage

1. Run the `main.py` script:

    ```bash
    python main.py
    ```

This script serves as the entry point for the application. When executed, it performs the following tasks:

- Creates the necessary database tables in the SQLite3 database (if they don't exist).
- Populates the SQLite3 and MongoDB databases with sample data from the `data.json` file.
- Demonstrates various CRUD operations on student and advisor records in both databases.
- Showcases the retrieval of student and advisor data based on different criteria.
- Generates and displays reports on the number of students per advisor and the number of advisors per student.

You can modify the `main.py` script to experiment with different operations or add your own functionality.

## File Structure

- `DB/`: Directory containing the database management code
  - `sqlite3_db.py`: Code for managing the SQLite3 database, including creating tables, executing queries, and performing CRUD operations.
  - `mongo_db.py`: Code for managing the MongoDB database, including creating collections, executing queries, and performing CRUD operations.
- `Models/`: Directory containing the model classes
  - `advisor.py`: Advisor model class, representing an advisor with attributes like name, surname, age, and a list of associated students.
  - `student.py`: Student model class, representing a student with attributes like name, surname, age, and GPA.
  - `studentAdvisor.py`: StudentAdvisor model class, used for managing the relationships between students and advisors.
- `Data/`: Directory containing sample data
  - `data.json`: JSON file with sample student and advisor data used to populate the databases.
- `main.py`: Main script to run the application, showcasing various operations and generating reports.
- `README.md`: This file, providing an overview of the project and instructions for installation and usage.
