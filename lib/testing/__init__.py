# lib/__init__.py
import sqlite3

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

# lib/department.py
from __init__ import CURSOR, CONN

class Department:
    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS departments;")
        CONN.commit()

    def save(self):
        CURSOR.execute("INSERT INTO departments (name, location) VALUES (?, ?)", (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        CURSOR.execute("UPDATE departments SET name = ?, location = ? WHERE id = ?", (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM departments WHERE id = ?", (self.id,))
        CONN.commit()

# lib/debug.py
from __init__ import CONN, CURSOR
from department import Department

Department.drop_table()
Department.create_table()

payroll = Department.create("Payroll", "Building A, 5th Floor")
print(payroll)

hr = Department.create("Human Resources", "Building C, East Wing")
print(hr)

hr.name = 'HR'
hr.location = "Building F, 10th Floor"
hr.update()
print(hr)

print("Delete Payroll")
payroll.delete()
print(payroll)
