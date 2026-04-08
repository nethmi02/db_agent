"""
setup_db.py
───────────
Run this script ONCE to create a sample SQLite database with realistic data.
This is only for learning/testing. In a real project, your database already exists.

Usage:
    python setup_db.py

What it creates:  sample.db
Tables:
    - students      (id, name, age, grade, city)
    - courses       (id, name, teacher, credits)
    - enrollments   (student_id, course_id, score, semester)
    - teachers      (id, name, subject, experience_years)
"""

import sqlite3
import os
import random

DB_PATH = "sample.db"

# ─── Sample Data ──────────────────────────────────────────────────────────────

STUDENTS = [
    ("Alice Johnson",   20, "A", "Colombo"),
    ("Bob Perera",      22, "B", "Kandy"),
    ("Chathuri Silva",  19, "A", "Galle"),
    ("David Fernando",  21, "C", "Colombo"),
    ("Emma Wijesinghe", 23, "B", "Matara"),
    ("Fathima Nizam",   20, "A", "Colombo"),
    ("Ganesh Kumar",    22, "D", "Jaffna"),
    ("Hasini Ranatunga",19, "B", "Kandy"),
    ("Ishan Bandara",   24, "C", "Colombo"),
    ("Janani Mendis",   21, "A", "Negombo"),
    ("Kevin De Silva",  20, "B", "Colombo"),
    ("Lakshmi Pillai",  22, "A", "Jaffna"),
    ("Mahen Siriwardena",23,"C", "Galle"),
    ("Nisha Perera",    19, "A", "Colombo"),
    ("Osanda Rathnayake",21,"B", "Kandy"),
]

TEACHERS = [
    ("Dr. Sunil Ariyaratne", "Mathematics",       15),
    ("Ms. Priya Jayawardena","English Literature", 8),
    ("Mr. Ranjith Kumara",   "Physics",            12),
    ("Dr. Amali Fernando",   "Computer Science",   10),
    ("Ms. Dilrukshi Perera", "Chemistry",          6),
]

COURSES = [
    ("Mathematics 101",     1, 3),   # (name, teacher_id, credits)
    ("English Literature",  2, 2),
    ("Physics Fundamentals",3, 4),
    ("Introduction to CS",  4, 3),
    ("Organic Chemistry",   5, 4),
    ("Advanced Math",       1, 3),
    ("Creative Writing",    2, 2),
    ("Quantum Physics",     3, 4),
]

SEMESTERS = ["2023-Fall", "2024-Spring", "2024-Fall", "2025-Spring"]


def create_tables(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        DROP TABLE IF EXISTS enrollments;
        DROP TABLE IF EXISTS courses;
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS teachers;

        CREATE TABLE teachers (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            name              TEXT    NOT NULL,
            subject           TEXT    NOT NULL,
            experience_years  INTEGER NOT NULL
        );

        CREATE TABLE students (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            age   INTEGER NOT NULL,
            grade TEXT    NOT NULL,   -- A, B, C, D
            city  TEXT    NOT NULL
        );

        CREATE TABLE courses (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL,
            teacher_id INTEGER NOT NULL,
            credits    INTEGER NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        );

        CREATE TABLE enrollments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL,
            course_id   INTEGER NOT NULL,
            score       REAL    NOT NULL,  -- 0.0 to 100.0
            semester    TEXT    NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id)  REFERENCES courses(id)
        );
    """)
    print("✅ Tables created.")


def seed_data(conn: sqlite3.Connection) -> None:
    # Insert teachers
    conn.executemany(
        "INSERT INTO teachers (name, subject, experience_years) VALUES (?, ?, ?)",
        TEACHERS
    )

    # Insert students
    conn.executemany(
        "INSERT INTO students (name, age, grade, city) VALUES (?, ?, ?, ?)",
        STUDENTS
    )

    # Insert courses
    conn.executemany(
        "INSERT INTO courses (name, teacher_id, credits) VALUES (?, ?, ?)",
        COURSES
    )

    # Insert enrollments — each student takes 3-5 random courses
    random.seed(42)  # so results are the same every time
    enrollments = []
    num_students = len(STUDENTS)
    num_courses  = len(COURSES)

    for student_id in range(1, num_students + 1):
        chosen_courses = random.sample(range(1, num_courses + 1), k=random.randint(3, 5))
        for course_id in chosen_courses:
            score    = round(random.uniform(40, 100), 1)
            semester = random.choice(SEMESTERS)
            enrollments.append((student_id, course_id, score, semester))

    conn.executemany(
        "INSERT INTO enrollments (student_id, course_id, score, semester) VALUES (?, ?, ?, ?)",
        enrollments
    )
    print(f"✅ Seeded {num_students} students, {len(TEACHERS)} teachers, "
          f"{num_courses} courses, {len(enrollments)} enrollments.")


def verify(conn: sqlite3.Connection) -> None:
    """Print a quick summary so you can see the data is there."""
    print("\n📊 Database Summary:")
    print("-" * 40)
    for table in ["teachers", "students", "courses", "enrollments"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:<15} → {count} rows")
    print("-" * 40)

    print("\n🔍 Sample: Top 5 students by average score")
    rows = conn.execute("""
        SELECT s.name, ROUND(AVG(e.score), 1) AS avg_score
        FROM students s
        JOIN enrollments e ON s.id = e.student_id
        GROUP BY s.id
        ORDER BY avg_score DESC
        LIMIT 5
    """).fetchall()
    for name, score in rows:
        print(f"  {name:<25} {score}")


def main() -> None:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"🗑️  Removed old {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn)
        seed_data(conn)
        conn.commit()
        verify(conn)
        print(f"\n🎉 Done! Database saved as: {DB_PATH}")
        print("   You can now set DATABASE_URL=sqlite:///./sample.db in your .env file")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
