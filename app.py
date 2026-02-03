from flask import Flask, render_template, request

app = Flask(__name__)

# Маълумоти парвозҳо
flights_data = [
    {"from": "Душанбе", "to": "Москва", "price": 2500, "date": "10.02.2026", "id": 1},
    {"from": "Душанбе", "to": "Истанбул", "price": 4200, "date": "11.02.2026", "id": 2},
    {"from": "Хуҷанд", "to": "Тошканд", "price": 850, "date": "12.02.2026", "id": 3},
    {"from": "Душанбе", "to": "Дубай", "price": 3500, "date": "13.02.2026", "id": 4}
]

@app.route('/')
def home():
    return render_template('index.html', flights=flights_data)

@app.route('/search', methods=['POST'])
def search():
    start = request.form.get('from', '').capitalize()
    end = request.form.get('to', '').capitalize()
    results = [f for f in flights_data if start in f['from'] and end in f['to']]
    return render_template('index.html', flights=results)

if __name__ == '__main__':
    app.run(debug=True)
