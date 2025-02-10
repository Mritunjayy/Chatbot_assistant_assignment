import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Create Employees table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL,
    Salary INTEGER NOT NULL,
    Hire_Date TEXT NOT NULL
)
''')

# Create Departments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Manager TEXT NOT NULL
)
''')

# Insert sample data
cursor.executemany('''
INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?)
''', [
    ('Alice', 'Sales', 50000, '2021-01-15'),
    ('Bob', 'Engineering', 70000, '2020-06-10'),
    ('Charlie', 'Marketing', 60000, '2022-03-20'),
    ('Ibrahim', 'Sales', 55000, '2021-02-15'),
    ('Anshul', 'Marketing', 65000, '2022-07-23'),
    ('Piyush', 'Engineering', 80000, '2021-03-10'),
    ('Berlin', 'Marketing', 60000, '2020-08-17')
])

cursor.executemany('''
INSERT INTO Departments (Name, Manager) VALUES (?, ?)
''', [
    ('Sales', 'Alice'),
    ('Engineering', 'Bob'),
    ('Marketing', 'Charlie')
])

# Commit and close connection
conn.commit()
conn.close()

print("Database setup complete!")
