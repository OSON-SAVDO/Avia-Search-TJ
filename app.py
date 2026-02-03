import sqlite3
from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

# Функсия барои пайваст шудан ба базаи маълумот
def get_db_connection():
    conn = sqlite3.connect('avia_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Сохтани ҷадвал ва иловаи маълумоти аввалия (Танҳо як бор иҷро мешавад)
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
            price INTEGER,
            buy_url TEXT
        )
    ''')
    
    # Илова кардани чиптаҳои намунавӣ
    sample_flights = [
        ('Somon Air', '✈️', 'Душанбе', 'Москва', '2026-02-10', 2500, 'https://www.somonair.com'),
        ('Ural Airlines', '🔴', 'Душанбе', 'Хуҷанд', '2026-02-11', 450, 'https://www.uralairlines.ru'),
        ('Turkish Airlines', '🇹🇷', 'Душанбе', 'Истанбул', '2026-02-12', 4200, 'https://www.turkishairlines.com'),
        ('Somon Air', '✈️', 'Хуҷанд', 'Дубай', '2026-02-13', 3100, 'https://www.somonair.com')
    ]
    
    conn.executemany('''
        INSERT INTO flights (airline, logo, from_city, to_city, date, price, buy_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_flights)
    
    conn.commit()
    conn.close()

# Оғози базаи маълумот ҳангоми ба кор даромадани барнома
init_db()

@app.route('/')
def index():
    # Гирифтани забон аз Cookies
    lang = request.cookies.get('language', 'tg')
    
    conn = get_db_connection()
    # Гирифтани чиптаҳо аз база
    flights = conn.execute('SELECT * FROM flights ORDER BY price ASC').fetchall()
    conn.close()
    
    return render_template('index.html', flights=flights, lang=lang)

@app.route('/search', methods=['POST'])
def search():
    lang = request.cookies.get('language', 'tg')
    start_city = request.form.get('from', '').strip()
    end_city = request.form.get('to', '').strip()
    
    conn = get_db_connection()
    # Ҷустуҷӯи динамикӣ дар базаи маълумот
    query = 'SELECT * FROM flights WHERE from_city LIKE ? AND to_city LIKE ?'
    results = conn.execute(query, ('%' + start_city + '%', '%' + end_city + '%')).fetchall()
    conn.close()
    
    return render_template('index.html', flights=results, lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
