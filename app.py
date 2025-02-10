from flask import Flask, request, jsonify, render_template
import sqlite3
import nltk
import re
from datetime import datetime
from itertools import chain

nltk.download('punkt')
nltk.download('punkt_tab')  # For tokenization
from nltk.tokenize import word_tokenize

app = Flask(__name__)

#connect to SQLite database
def connect_db():
    return sqlite3.connect("company.db")

#------------------------------------------------------------

def get_department_from_query(query):
    departments = {"sales": "Sales", "engineering": "Engineering", "marketing": "Marketing"}  # Normalized
    for word in word_tokenize(query.lower()):
        if word in departments:
            return departments[word]
    return None

def generate_ngrams(query, n=3):
    words = word_tokenize(query.lower())  # Tokenize into words
    ngrams = list(chain.from_iterable(
        zip(*(words[i:] for i in range(n))) for n in range(1, len(words) + 1)
    ))  # Generate n-word tokens
    return [" ".join(ngram) for ngram in ngrams]

def process_query(user_query):
    # tokens = word_tokenize(user_query.lower())
    tokens = generate_ngrams(user_query, n=3)  # n = n-grams
    print(tokens)
    department = get_department_from_query(user_query)
    print(department)
    
    if "employees" in tokens and department:
        if "name" in tokens :
            sql_query = f"SELECT Name FROM Employees WHERE Department='{department}'"
            return sql_query
        elif "salary" in tokens:
            if "total" in tokens:
                sql_query = f"SELECT SUM(Salary) FROM Employees WHERE Department='{department}'"
            else:
                sql_query = f"SELECT Name, Salary FROM Employees WHERE Department=?"
            return sql_query
        elif "hire date" in tokens or "hiring date" in tokens:
            sql_query = f"SELECT Name, Hire_Date FROM Employees WHERE Department='{department}'"
            return sql_query
    
    elif "manager" in tokens and "department" in tokens and department:
        sql_query = f"SELECT Manager FROM Departments WHERE Name='{department}'"
        return sql_query
    
    elif "hired after" in user_query:
        match = re.search(r"hired after (\d{4}-\d{2}-\d{2})", user_query, re.IGNORECASE)
        if match:
            date = match.group(1)
            date_object = datetime.strptime(date, "%Y-%m-%d")
            date_only = date_object.date()
            sql_query = f"SELECT Name FROM Employees WHERE Hire_Date > '{date_only}'"
            return sql_query
    
    elif "hired before" in user_query:
        match = re.search(r"hired before (\d{4}-\d{2}-\d{2})", user_query, re.IGNORECASE)
        if match:
            date = match.group(1)
            date_object = datetime.strptime(date, "%Y-%m-%d")
            date_only = date_object.date()
            print(date_only)
            sql_query = f"SELECT Name FROM Employees WHERE Hire_Date < '{date_only}'"
            return sql_query
    
    elif "difference in hiring" in user_query:
        match = re.findall(r"(\w+) and (\w+)", user_query)
        if match:
            emp1, emp2 = match[0]
            sql_query = f"SELECT Name, Hire_Date FROM Employees WHERE Name IN ('{emp1}', '{emp2}')"
            return sql_query
    
    elif ((("employees" in tokens) or ("salary" in tokens) or ("hire date" in tokens) or ("department" in tokens)) and ("manager" in tokens)) or department:
        sql_query = """
        SELECT Employees.Name, Employees.Department, Employees.Salary, Employees.Hire_Date, Departments.Manager
        FROM Employees
        JOIN Departments ON Employees.Department = Departments.Name
        WHERE Employees.Name != Departments.Manager
        """
        return sql_query
    
    elif "manager" in tokens and "employee" in tokens:
        match = re.search(r"id (\d+)", user_query, re.IGNORECASE)
        if match:
            emp_id = match.group(1)
            sql_query = f"""
            SELECT Departments.Manager FROM Employees 
            JOIN Departments ON Employees.Department = Departments.Name 
            WHERE Employees.ID = '{emp_id}'
            """
            return sql_query
        
    elif "show me all employees in" in user_query and department:
        sql_query = f"SELECT Name FROM Employees WHERE Department='{department}'"
        return sql_query
    
    elif "who is the manager of" in user_query and department:
        sql_query = f"SELECT Manager FROM Departments WHERE Name='{department}'"
        return sql_query
    
    elif "list all employees hired after" in user_query:
        match = re.search(r"hired after (\d{4}-\d{2}-\d{2})", user_query, re.IGNORECASE)
        if match:
            date = match.group(1)
            date_object = datetime.strptime(date, "%Y-%m-%d")
            date_only = date_object.date()
            sql_query = f"SELECT Name FROM Employees WHERE Hire_Date > '{date_only}'"
            return sql_query
    
    elif "total salary expense for" in user_query and department:
        sql_query = f"SELECT SUM(Salary) FROM Employees WHERE Department='{department}'"        
        return sql_query
    
    return None

#------------------------------------------------------------
    
@app.route("/")
def home():
    return render_template("index.html")


# API endpoint for handling chat queries
@app.route("/query", methods=["GET","POST"])
def query_db():
    data = request.json
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    sql_query = process_query(user_query)
    if not sql_query:
        return jsonify({"error": "Unsupported query format"}), 400
    print(sql_query)
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print(results)
        conn.close()

        if results:
            return jsonify({"response": results})
        else:
            return jsonify({"response": "No matching records found."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#API Endpoint to list all the employees from EMployees table
@app.route("/employees", methods=["GET"])
def get_employees():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees;")
    employees = cursor.fetchall()
    conn.close()
    
    return jsonify({"employees": employees})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
