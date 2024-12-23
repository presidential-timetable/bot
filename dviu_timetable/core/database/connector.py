import sqlite3


connection = sqlite3.connect('dviu_timetable.bot.db')

connection.cursor().execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER NOT NULL,
    telegram_name TEXT NOT NULL,
    telegram_username TEXT,
    name TEXT NOT NULL,
    activated_on INTEGER NOT NULL,
    role TEXT NOT NULL,
    domain_id INTEGER NOT NULL,
    faculty_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL
) 
""")
