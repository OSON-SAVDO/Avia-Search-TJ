import sqlite3
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

# Функсия барои пайваст шудан ба базаи маълумот
def get_db_connection():
    conn = sqlite3.connect('flights.db')
    conn.row_factory = sqlite3.Row
    return conn

# Сохтани базаи маълумот ва ҷадвали чиптаҳо (Танҳо як бор иҷро мешавад)
def init_db():
    conn = get_db_connection()
    conn.execute('DROP TABLE IF EXISTS flights')
    conn.execute('''
        CREATE TABLE flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airline TEXT,
            logo TEXT,
            departure_city TEXT,
            arrival_city TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            duration TEXT,
            price INTEGER,
            date TEXT
        )
    ''')
    # Илова кардани чиптаҳои ҳақиқӣ
    flights = [
        ('Somon Air', '✈️', 'Душанбе', 'Москва', '08:00', '11:30', '4с 30д', 2500, '2026-02-10'),
        ('Ural Airlines', '🔴', 'Душанбе', 'Москва', '14:20', '17:50', '4с 30д', 2300, '2026-02-10'),
        ('Turkish Airlines', '🇹🇷', 'Душанбе', 'Истанбул', '05:45', '09:20', '5с 35д', 4200, '2026-02-11'),
        ('Somon Air', '✈️', 'Хуҷанд', 'Дубай', '22:00', '01:15', '3с 15д', 3100, '2026-02-12')
    ]
    conn.executemany('INSERT INTO flights (airline, logo, departure_city, arrival_city, departure_time, arrival_time, duration, price, date) VALUES (?,?,?,?,?,?,?,?,?)', flights)
    conn.commit()
    conn.close()

init_db() # Инро ҳангоми оғоз кор меандозем

translations = {
    'tg': {'from': 'Аз куҷо', 'to': 'Ба куҷо', 'date': 'Сана', 'search': 'Ёфтани чипта', 'currency': 'TJS'},
    'ru': {'from': 'Откуда', 'to': 'Куда', 'date': 'Дата', 'search': 'Найти билеты', 'currency': 'TJS'}
}

@app.route('/')
def home():
    lang = request.cookies.get('language', 'tg')
    conn = get_db_connection()
    flights = conn.execute('SELECT * FROM flights LIMIT 3').fetchall()
    conn.close()
    return render_template('index.html', flights=flights, t=translations[lang], lang=lang)

@app.route('/search', methods=['POST'])
def search():
    lang = request.cookies.get('language', 'tg')
    start = request.form.get('from', '').strip()
    end = request.form.get('to', '').strip()
    date = request.form.get('departure_date')

    conn = get_db_connection()
    query = 'SELECT * FROM flights WHERE departure_city LIKE ? AND arrival_city LIKE ? AND date = ?'
    results = conn.execute(query, ('%'+start+'%', '%'+end+'%', date)).fetchall()
    conn.close()
    
    return render_template('index.html', flights=results, t=translations[lang], lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
