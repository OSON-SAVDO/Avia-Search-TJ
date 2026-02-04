import requests
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# --- МАЪЛУМОТИ ШАХСӢ ---
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'
MARKER = '701004'

AIRPORTS_DB = {
    "ДУШАНБЕ": "DYU", "МОСКВА": "MOW", "ХУҶАНД": "LBD",
    "ИСТАНБУЛ": "IST", "САНКТ-ПЕТЕРБУРГ": "LED", "ДУБАЙ": "DXB",
    "ТОШКЕНТ": "TAS", "АЛМАТЫ": "ALA", "КУЛОБ": "TJU"
}

@app.route('/')
def index():
    return render_template('index.html', flights=None)

@app.route('/search', methods=['POST'])
def search():
    # Гирифтани маълумот аз форма
    from_city = request.form.get('from_city', '').strip().upper()
    to_city = request.form.get('to_city', '').strip().upper()
    depart_date = request.form.get('depart_date')
    
    # Мусофирон
    adults = request.form.get('adults', '1')
    children = request.form.get('children', '0')
    infants = request.form.get('infants', '0')

    origin = AIRPORTS_DB.get(from_city)
    destination = AIRPORTS_DB.get(to_city)

    if not origin or not destination:
        return render_template('index.html', error="Шаҳр ёфт нашуд. Лутфан номро дуруст нависед.")

    # API барои ҷустуҷӯи нархҳо
    url = "https://api.travelpayouts.com/v3/prices_for_dates"
    params = {
        'origin': origin,
        'destination': destination,
        'departure_at': depart_date,
        'token': API_TOKEN,
        'currency': 'tjs',
        'sorting': 'price',
        'limit': 20
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        flights_list = []

        if data.get('success') and 'data' in data:
            for f in data['data']:
                d_at = f.get('departure_at', '')
                # Сохтани линки харид бо шумораи мусофирон
                # Формат: /SEARCH + ORIGIN + DATE + DESTINATION + PASSENGERS
                date_part = f"{d_at[8:10]}{d_at[5:7]}"
                buy_url = f"https://www.aviasales.tj/search/{origin}{date_part}{destination}{adults}{children}{infants}?marker={MARKER}"
                
                flights_list.append({
                    'airline': f.get('airline'),
                    'price': f.get('price'),
                    'date': d_at[:10],
                    'time': d_at[11:16],
                    'transfers': f.get('transfers'),
                    'duration': f.get('duration'), # Давомнокии парвоз (дақиқа)
                    'has_baggage': f.get('has_baggage', False),
                    'buy_url': buy_url
                })
        
        return render_template('index.html', flights=flights_list, origin=from_city, destination=to_city)
    except Exception as e:
        return f"Хатогии техникӣ: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
