#!/usr/bin/env python3

import cgi
import cgitb
import sqlite3

cgitb.enable()

print("Content-Type: text/html")
print()

# Connect to SQLite database
conn = sqlite3.connect('/var/www/cgi-bin/poll.db')
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS polls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    votes INTEGER DEFAULT 0,
    FOREIGN KEY(poll_id) REFERENCES polls(id)
)
''')

form = cgi.FieldStorage()
action = form.getvalue("action", "")

if action == "create_poll":
    question = form.getvalue("question", "")
    options = form.getlist("options")
    cursor.execute('INSERT INTO polls (question) VALUES (?)', (question,))
    poll_id = cursor.lastrowid
    for option in options:
        cursor.execute('INSERT INTO options (poll_id, option_text) VALUES (?, ?)', (poll_id, option))
    conn.commit()

elif action == "vote":
    option_id = int(form.getvalue("option_id", ""))
    cursor.execute('UPDATE options SET votes = votes + 1 WHERE id = ?', (option_id,))
    conn.commit()

elif action == "view_results":
    poll_id = int(form.getvalue("poll_id", ""))
    cursor.execute('SELECT question FROM polls WHERE id = ?', (poll_id,))
    question = cursor.fetchone()[0]
    cursor.execute('SELECT option_text, votes FROM options WHERE poll_id = ?', (poll_id,))
    options = cursor.fetchall()
    print(f"""
    <html>
    <head>
        <title>Poll Results</title>
        <link rel="stylesheet" type="text/css" href="/style.css">
    </head>
    <body>
        <h1>{question}</h1>
        <ul>
    """)
    for option in options:
        print(f"<li>{option[0]}: {option[1]} votes</li>")
    print("""
        </ul>
        <a href="/index.html">Back to Home</a>
    </body>
    </html>
    """)
    conn.close()
    exit()

print("""
<html>
<head>
    <title>Online Polling System</title>
    <link rel="stylesheet" type="text/css" href="/style.css">
</head>
<body>
    <h1>Create a Poll</h1>
    <form action="/cgi-bin/poll.py" method="post">
        <input type="hidden" name="action" value="create_poll">
        <label for="question">Question:</label>
        <input type="text" id="question" name="question" required><br>
        <label for="option1">Option 1:</label>
        <input type="text" id="option1" name="options" required><br>
        <label for="option2">Option 2:</label>
        <input type="text" id="option2" name="options" required><br>
        <label for="option3">Option 3:</label>
        <input type="text" id="option3" name="options" required><br>
        <input type="submit" value="Create Poll">
    </form>
    <h1>Current Polls</h1>
    <ul>
""")

cursor.execute('SELECT id, question FROM polls')
polls = cursor.fetchall()
for poll in polls:
    print(f"""
        <li>
            <strong>{poll[1]}</strong><br>
            <form action="/cgi-bin/poll.py" method="post">
                <input type="hidden" name="action" value="vote">
                <input type="hidden" name="poll_id" value="{poll[0]}">
    """)
    cursor.execute('SELECT id, option_text FROM options WHERE poll_id = ?', (poll[0],))
    options = cursor.fetchall()
    for option in options:
        print(f'<input type="radio" name="option_id" value="{option[0]}" required> {option[1]}<br>')
    print(f"""
                <input type="submit" value="Vote">
            </form>
            <form action="/cgi-bin/poll.py" method="post">
                <input type="hidden" name="action" value="view_results">
                <input type="hidden" name="poll_id" value="{poll[0]}">
                <input type="submit" value="View Results">
            </form>
        </li>
    """)

print("""
    </ul>
</body>
</html>
""")

conn.close()

