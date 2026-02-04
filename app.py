import requests
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# МАЪЛУМОТИ ХУДРО ИНҶО ГУЗОРЕД
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'
MARKER = '701004'

# Рӯйхати ислоҳшудаи фурудгоҳҳо
AIRPORTS_DB = {
    "ДУШАНБЕ": "DYU",
    "МОСКВА": "MOW",
    "ХУҶАНД": "LBD",
    "ИСТАНБУЛ": "IST",
    "САНКТ-ПЕТЕРБУРГ": "LED",
    "ЕКАТЕРИНБУРГ": "SVX",
    "НОВОСИБИРСК: "OVB",
    "ҚАЗОН": "KZN",
    "АЛМАТЫ": "ALA",
    "ТОШКЕНТ": "TAS",
    "ДУБАЙ": "DXB",
    "КУЛОБ": "TJU",
    "БОХТАР": "KQT"
}

@app.route('/')
def index():
    return render_template('index.html', flights=None)

@app.route('/search', methods=['POST'])
def search():
    from_input = request.form.get('from_display', '').strip().upper()
    to_input = request.form.get('to_display', '').strip().upper()
    
    origin = AIRPORTS_DB.get(from_input)
    destination = AIRPORTS_DB.get(to_input)

    if not origin or not destination:
        return render_template('index.html', error="Шаҳр ёфт нашуд. Лутфан номро дуруст нависед.")

    url = "https://api.travelpayouts.com/v3/prices_for_dates"
    params = {
        'origin': origin,
        'destination': destination,
        'token': API_TOKEN,
        'currency': 'tjs',
        'unique': 'true',
        'limit': 10
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        flights_list = []
        if data.get('success') and 'data' in data:
            for f in data['data']:
                date_str = f.get('departure_at', '')
                buy_url = f"https://www.aviasales.tj/search/{origin}{date_str[8:10]}{date_str[5:7]}{destination}1?marker={MARKER}"
                flights_list.append({
                    'airline': f.get('airline'),
                    'price': f.get('price'),
                    'date': date_str[:10],
                    'type': "Мустақим" if f.get('transfers') == 0 else f"Таваққуф: {f.get('transfers')}",
                    'from_city': from_input.capitalize(),
                    'to_city': to_input.capitalize(),
                    'origin_code': origin,
                    'destination_code': destination,
                    'buy_url': buy_url
                })
        
        if not flights_list:
            return render_template('index.html', error="Чипта ёфт нашуд.")
        return render_template('index.html', flights=flights_list)
    except:
        return "Хатогии техникӣ"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
