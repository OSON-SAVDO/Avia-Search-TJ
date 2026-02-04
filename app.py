import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'
MARKER = '701004'

@app.route('/')
def index():
    return render_template('index.html', flights=None)

@app.route('/search', methods=['POST'])
def search():
    origin = request.form.get('from') # Коди IATA аз hidden input
    destination = request.form.get('to')
    from_name = request.form.get('from_display')
    to_name = request.form.get('to_display')

    if not origin or not destination:
        return render_template('index.html', error="Лутфан шаҳрро аз рӯйхат интихоб кунед.")

    url = "https://api.travelpayouts.com/v1/prices/cheap"
    params = {'origin': origin, 'destination': destination, 'token': API_TOKEN, 'currency': 'tjs'}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        flights_list = []
        if data.get('success') and destination in data.get('data', {}):
            results = data['data'][destination]
            for key, f in results.items():
                date_str = f['departure_at']
                search_url = f"https://www.aviasales.tj/search/{origin}{date_str[8:10]}{date_str[5:7]}{destination}1?marker={MARKER}"
                flights_list.append({
                    'airline': f.get('airline'),
                    'price': f.get('price'),
                    'date': date_str,
                    'type': "Мустақим" if f.get('transfers') == 0 else f"Таваққуф: {f.get('transfers')}",
                    'from_city': from_name,
                    'to_city': to_name,
                    'origin_code': origin,
                    'destination_airport': destination,
                    'buy_url': search_url
                })
        return render_template('index.html', flights=flights_list, searched=True)
    except:
        return "Хатогии техникӣ"

if __name__ == '__main__':
    app.run(debug=True)
