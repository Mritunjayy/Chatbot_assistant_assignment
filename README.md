# Chat Assistant with SQLite

This is a natural language chat assistant that processes user queries, converts them into SQL queries, and fetches results from an SQLite database. It supports department-based employee queries, salary calculations, hire date comparisons, and more.

## Features
- Process natural language queries and convert them to SQL.
- Retrieve employee details based on department, salary, or hire date.
- Fetch department managers and salary expenses.
- Compare employee hiring dates.
- Handle errors gracefully and return formatted responses.

## How It Works After Deployment
1. Users interact with the web-based UI.
2. The frontend sends the query to the backend.
3. The backend processes the query using `process_query()`.
4. The SQL query is executed on an SQLite database.
5. Results are returned and displayed in the UI.

## Running the Project Locally
### Prerequisites
- Python 3.x
- Flask
- SQLite3
- NLTK

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <project_directory>
   ```
2. Install dependencies:
   ```sh
   pip install flask nltk sqlite3
   ```
3. Run the Flask server:
   ```sh
   python app.py
   ```
4. Open `index.html` in a browser or use `http://127.0.0.1:5000`.

## API Endpoints
- `POST /query` - Accepts user queries and returns responses.

## Known Limitations & Future Improvements
- **Synonym Handling:** The assistant might not recognize different phrasing.
- **Complex Queries:** Currently supports basic SQL queries but needs improvement for complex joins and sub-queries.
- **Frontend Styling:** Can be enhanced for better UX.
- **Database Scalability:** Currently works with SQLite; migrating to PostgreSQL or MySQL would improve performance for large datasets.

## Contributors
- Mritunjay Pandey (pmritunjay947@gmail.com)

## PS- Any corrections and contributionshighly welcomed!! (:

