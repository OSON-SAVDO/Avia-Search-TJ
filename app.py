import sqlite3
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('aviasales_clone.db')
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
            buy_url TEXT  -- Линки шарикии шумо барои ҳар як чипта
        )
    ''')
    
    # Намунаи чиптаҳо бо линкҳои гуногун
    # Дар оянда ба ҷои ин линкҳо, шумо линки Travelpayouts-ро мегузоред
    flights = [
        ('Somon Air', '✈️', 'Душанбе', 'Москва', '2026-02-10', '08:00', '11:30', '4с 30д', 2500, 'https://www.aviasales.tj/search/DYU1002MOW1'),
        ('Ural Airlines', '🔴', 'Душанбе', 'Москва', '2026-02-10', '14:20', '17:50', '4с 30д', 2300, 'https://www.uralairlines.ru'),
        ('Turkish Airlines', '🇹🇷', 'Душанбе', 'Истанбул', '2026-02-11', '05:45', '09:20', '5с 35д', 4200, 'https://www.turkishairlines.com')
    ]
    conn.executemany('''INSERT INTO flights 
        (airline, logo, from_city, to_city, date, dep_time, arr_time, duration, price, buy_url) 
        VALUES (?,?,?,?,?,?,?,?,?,?)''', flights)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    lang = request.cookies.get('language', 'tg')
    conn = get_db_connection()
    flights = conn.execute('SELECT * FROM flights ORDER BY price ASC').fetchall()
    conn.close()
    
    # Луғати тарҷумаи интерфейс
    t = {
        'tg': {'search': 'Ҷустуҷӯ', 'buy': 'ХАРИДАН', 'from': 'Аз куҷо', 'to': 'Ба куҷо'},
        'ru': {'search': 'Поиск', 'buy': 'КУПИТЬ', 'from': 'Откуда', 'to': 'Куда'}
    }
    return render_template('index.html', flights=flights, t=t[lang], lang=lang)

@app.route('/search', methods=['POST'])
def search():
    lang = request.cookies.get('language', 'tg')
    # Мантиқи ҷустуҷӯ дар инҷо...
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
