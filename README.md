# AI Agent for SQL Queries

This project is an intelligent agent that converts natural language questions into SQL queries, executes those queries on a SQLite database, and returns the results through a user-friendly web interface.
##Features

-Simple web interface to submit questions about the data.
-Automatic conversion of questions into SQL using an LLM (OpenAI GPT-4o-mini).
-Secure query execution (only SELECT statements allowed).
-Displays the generated SQL and the query results.

## Project Structure
- `app.py`: Flask backend, integrates with LLM and executes queries.
- `init_db.py`: Script to create and populate the SQLite database.
- `templates/index.html`: Web interface for interacting with the agent.
- `requirements.txt`: Project dependencies.
- `.env`: OpenAI API key.

## How to use

1. Install the dependencies:

``bash
pip install -r requirements.txt

```
2. Configure your OpenAI key in `.env`.

3. Initialize the database:

``bash
python init_db.py

```
4. Run the Flask server:

``bash
python app.py

```
5. Access `http://localhost:8080` in your browser.

## Notes
- Only SELECT commands are allowed for security reasons.

- The LLM model generates SQL based on the database schema.

- The project can be expanded to other databases or commands.

## Example of use
Question: "List the registered products"

Generated SQL:

```sql
SELECT * FROM products;

```

Result: (list of products, if the table exists)

---

Developed by Roger, 2026.
