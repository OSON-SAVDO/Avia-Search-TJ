import sqlite3
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# Пайвастшавӣ ба база
def get_db_connection():
    conn = sqlite3.connect('business_avia.db')
    conn.row_factory = sqlite3.Row
    return conn

# Сохтани базаи маълумот
def init_db():
    conn = get_db_connection()
    conn.execute('DROP TABLE IF EXISTS tickets')
    conn.execute('''
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airline TEXT,
            logo TEXT,
            from_city TEXT,
            to_city TEXT,
            date TEXT,
            time TEXT,
            price INTEGER, -- Нархи фурӯши шумо
            seats INTEGER, -- Миқдори чиптаҳое ки харидед
            wa_number TEXT -- Рақами WhatsApp-и шумо
        )
    ''')
    # Намунаи аввалини чиптаи шумо
    conn.execute('''INSERT INTO tickets (airline, logo, from_city, to_city, date, time, price, seats, wa_number)
                    VALUES (?,?,?,?,?,?,?,?,?)''', 
                 ('Ural Airlines', '🔴', 'Душанбе', 'Москва', '2026-02-15', '10:00', 2600, 80, '992900000000'))
    conn.commit()
    conn.close()

init_db()

translations = {
    'tg': {'from': 'Аз куҷо', 'to': 'Ба куҷо', 'date': 'Сана', 'search': 'Ҷустуҷӯ', 'buy': 'БРОН ДАР WHATSAPP', 'seats': 'Ҷойҳои боқимонда'},
    'ru': {'from': 'Откуда', 'to': 'Куда', 'date': 'Дата', 'search': 'Поиск', 'buy': 'БРОНЬ В WHATSAPP', 'seats': 'Осталось мест'}
}

@app.route('/')
def home():
    lang = request.cookies.get('language', 'tg')
    conn = get_db_connection()
    tickets = conn.execute('SELECT * FROM tickets WHERE seats > 0').fetchall()
    conn.close()
    return render_template('index.html', tickets=tickets, t=translations[lang], lang=lang)

@app.route('/search', methods=['POST'])
def search():
    lang = request.cookies.get('language', 'tg')
    start = request.form.get('from', '').capitalize()
    end = request.form.get('to', '').capitalize()
    date = request.form.get('departure_date')
    
    conn = get_db_connection()
    query = 'SELECT * FROM tickets WHERE from_city LIKE ? AND to_city LIKE ? AND date = ? AND seats > 0'
    results = conn.execute(query, ('%'+start+'%', '%'+end+'%', date)).fetchall()
    conn.close()
    return render_template('index.html', tickets=results, t=translations[lang], lang=lang)

# --- ПАНЕЛИ АДМИН БАРОИ ШУМО ---
@app.route('/admin')
def admin_panel():
    conn = get_db_connection()
    tickets = conn.execute('SELECT * FROM tickets').fetchall()
    conn.close()
    return render_template('admin.html', tickets=tickets)

@app.route('/admin/add', methods=['POST'])
def add_ticket():
    data = request.form
    conn = get_db_connection()
    conn.execute('''INSERT INTO tickets (airline, logo, from_city, to_city, date, time, price, seats, wa_number)
                    VALUES (?,?,?,?,?,?,?,?,?)''', 
                 (data['airline'], data['logo'], data['from'], data['to'], data['date'], data['time'], data['price'], data['seats'], data['wa']))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)
