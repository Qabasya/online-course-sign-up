import  sqlite3

DB_NAME = 'sign_up_bot.db'
DB_PATH = f'db/{DB_NAME}'

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute(f"""
           SELECT reg_date 
           FROM clients WHERE datetime (reg_date) > datetime('now', '-1 day') 
       """)
    rows = cursor.fetchall()

print(rows)


