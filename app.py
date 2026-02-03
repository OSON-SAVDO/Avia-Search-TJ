from flask import Flask, render_template, request

app = Flask(__name__)

# Маълумоти намунавӣ (Database)
flights_data = [
    {"from": "Душанбе", "to": "Москва", "price": 2500, "date": "2026-02-10"},
    {"from": "Душанбе", "to": "Истанбул", "price": 4200, "date": "2026-02-11"},
    {"from": "Хуҷанд", "to": "Тошканд", "price": 850, "date": "2026-02-12"},
    {"from": "Душанбе", "to": "Дубай", "price": 3500, "date": "2026-02-13"},
    {"from": "Кӯлоб", "to": "Москва", "price": 2700, "date": "2026-02-15"}
]

@app.route('/')
def home():
    # Ҳангоми аввал ворид шудан ҳамаи чиптаҳоро нишон медиҳем
    return render_template('index.html', flights=flights_data)

@app.route('/search', methods=['POST'])
def search():
    # Гирифтани маълумот аз форма
    start = request.form.get('from', '').strip().capitalize()
    end = request.form.get('to', '').strip().capitalize()
    selected_date = request.form.get('departure_date')
    
    # Мантиқи ҷустуҷӯ
    # Мо чиптаҳоеро меёбем, ки ба шаҳри воридшуда мувофиқанд
    results = []
    for f in flights_data:
        if start in f['from'] and end in f['to']:
            # Агар корбар санаро интихоб карда бошад, метавонед филтри санаро ҳам илова кунед
            results.append(f)
    
    return render_template('index.html', flights=results)

if __name__ == '__main__':
    # Ин барои кор дар компютери шумо ва сервер
    app.run(debug=False)
