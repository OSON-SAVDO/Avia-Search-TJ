import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- КОНФИГУРАЦИЯ ---
TOKEN = "71876b59812fee6e1539f9365e6a12dd" 
MARKER = "701004"

CITY_CODES = {
    "душанбе": "DYU", "худжанд": "LBD", "куляб": "TJU",
    "москва": "MOW", "санкт-петербург": "LED", "стамбул": "IST",
    "дубай": "DXB", "ташкент": "TAS", "алматы": "ALA", "анкара": "ESB"
}

def get_flights(origin, destination, date=None):
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_at": date,
        "currency": "rub",
        "sorting": "price",
        "direct": "false",
        "limit": 10,
        "token": TOKEN
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('data', [])
        return []
    except:
        return []

@app.route('/')
def index():
    return render_template('index.html', flights=[])

@app.route('/search', methods=['POST'])
def search():
    from_input = request.form.get('from', '').strip().lower()
    to_input = request.form.get('to', '').strip().lower()
    date = request.form.get('date')
    
    origin = CITY_CODES.get(from_input, from_input.upper())
    destination = CITY_CODES.get(to_input, to_input.upper())
    
    flights = get_flights(origin, destination, date)
    return render_template('index.html', flights=flights, marker=MARKER)

if __name__ == '__main__':
    app.run(debug=True)
