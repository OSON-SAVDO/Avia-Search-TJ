import sqlite3
from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('avia_business.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('DROP TABLE IF EXISTS flights')
    conn.execute('''
        CREATE TABLE flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airline TEXT,
            logo TEXT,
            from_city TEXT,
            to_city TEXT,
            date TEXT,
            dep_time TEXT,
            arr_time TEXT,
            duration TEXT,
            price INTEGER,
            is_direct INTEGER, -- 1 барои прямой, 0 барои пересадка
            buy_url TEXT
        )
    ''')
    
    # Намунаи маълумот
    flights = [
        ('Somon Air', '✈️', 'Душанбе', 'Москва', '2026-02-10', '08:00', '11:30', '4с 30д', 2500, 1, 'https://www.aviasales.tj'),
        ('Ural Airlines', '🔴', 'Душанбе', 'Москва', '2026-02-12', '14:20', '17:50', '4с 30д', 2300, 1, 'https://www.uralairlines.ru'),
        ('UTair', '🔷', 'Душанбе', 'Тюмен', '2026-02-15', '10:00', '14:00', '4с', 2100, 1, 'https://www.utair.ru'),
        ('Turkish Airlines', '🇹🇷', 'Душанбе', 'Истанбул', '2026-02-11', '05:45', '09:20', '5с 35д', 4200, 0, 'https://www.turkishairlines.com')
    ]
    conn.executemany('''INSERT INTO flights 
        (airline, logo, from_city, to_city, date, dep_time, arr_time, duration, price, is_direct, buy_url) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?)''', flights)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    lang = request.cookies.get('language', 'tg')
    conn = get_db_connection()
    flights = conn.execute('SELECT * FROM flights ORDER BY price ASC LIMIT 10').fetchall()
    conn.close()
    return render_template('index.html', flights=flights, lang=lang)

@app.route('/search', methods=['POST'])
def search():
    lang = request.cookies.get('language', 'tg')
    from_c = request.form.get('from', '').strip()
    to_c = request.form.get('to', '').strip()
    date = request.form.get('departure_date')
    direct_only = request.form.get('direct_only')

    conn = get_db_connection()
    query = 'SELECT * FROM flights WHERE from_city LIKE ? AND to_city LIKE ?'
    params = ['%' + from_c + '%', '%' + to_c + '%']

    if date:
        query += ' AND date = ?'
        params.append(date)
    
    if direct_only == '1':
        query += ' AND is_direct = 1'
    
    query += ' ORDER BY price ASC'
    results = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('index.html', flights=results, lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
