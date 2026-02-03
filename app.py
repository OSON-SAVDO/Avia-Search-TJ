import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# ↓↓↓ ТОКЕНИ ХУДРО ДАР ИН ҶО ГУЗОРЕД ↓↓↓
TOKEN = "71876b59812fee6e1539f9365e6a12dd" 
MARKER = "701004" # Маркери шумо аз скриншотҳо

# Луғати кодҳои шаҳрҳо барои ҷустуҷӯ
CITY_CODES = {
    "Душанбе": "DYU", "Хуҷанд": "LBD", "Москва": "MOW", 
    "Санкт-Петербург": "LED", "Истанбул": "IST", "Дубай": "DXB",
    "Тошканд": "TAS", "Тюмен": "TJM", "Алмати": "ALA"
}

def get_flights(origin, destination, date=None):
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {
        "origin": origin, "destination": destination,
        "departure_at": date, "currency": "tjs",
        "sorting": "price", "direct": "false",
        "limit": 10, "token": TOKEN
    }
    try:
        response = requests.get(url, params=params)
        return response.json().get('data', [])
    except:
        return []

@app.route('/')
def index():
    return render_template('index.html', flights=[])

@app.route('/search', methods=['POST'])
def search():
    from_city = request.form.get('from', 'Душанбе')
    to_city = request.form.get('to', 'Москва')
    date = request.form.get('departure_date')
    
    origin = CITY_CODES.get(from_city, "DYU")
    dest = CITY_CODES.get(to_city, "MOW")
    
    flights = get_flights(origin, dest, date)
    return render_template('index.html', flights=flights, marker=MARKER)

if __name__ == '__main__':
    app.run(debug=True)
