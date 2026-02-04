import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# МАЪЛУМОТИ ХУДРО ИНҶО ГУЗОРЕД
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'
MARKER = '701004'

def get_iata_code(city_name):
    """Функсия барои табдил додани номи шаҳр ба коди IATA"""
    try:
        url = f"https://autocomplete.travelpayouts.com/japi/bins/autocomplete?term={city_name}&locale=ru&types[]=city"
        response = requests.get(url)
        data = response.json()
        if data and len(data) > 0:
            return data[0]['code'] # Коди аввалини ёфтшударо бармегардонад
    except:
        return None
    return None

@app.route('/')
def index():
    return render_template('index.html', flights=None)

@app.route('/search', methods=['POST'])
def search():
    from_city_name = request.form.get('from', '').strip()
    to_city_name = request.form.get('to', '').strip()
    
    # Табдил ба кодҳои IATA
    origin = get_iata_code(from_city_name)
    destination = get_iata_code(to_city_name)
    
    if not origin or not destination:
        return render_template('index.html', flights=[], error="Шаҳр ёфт нашуд. Лутфан номро дуруст нависед.")

    # API барои гирифтани чиптаҳо аз тамоми ҷаҳон
    url = "https://api.travelpayouts.com/v1/prices/cheap"
    params = {
        'origin': origin,
        'destination': destination,
        'token': API_TOKEN,
        'currency': 'tjs'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        flights_list = []
        if data.get('success') and destination in data.get('data', {}):
            results = data['data'][destination]
            
            for key, flight in results.items():
                date_str = flight['departure_at']
                day = date_str[8:10]
                month = date_str[5:7]
                
                # Линки шарикӣ
                search_url = f"https://www.aviasales.tj/search/{origin}{day}{month}{destination}1?marker={MARKER}"
                
                flights_list.append({
                    'airline': flight.get('airline'),
                    'price': flight.get('price'),
                    'date': date_str,
                    'from_city': from_city_name.capitalize(),
                    'to_city': to_city_name.capitalize(),
                    'buy_url': search_url
                })
        
        return render_template('index.html', flights=flights_list, searched=True)
    except Exception as e:
        return f"Хатогии техникӣ: {e}"

@app.route('/ticket/<path:info>')
def ticket_details(info):
    parts = info.split('|')
    ticket = {
        'airline': parts[0], 'price': parts[1], 'from_city': parts[2],
        'to_city': parts[3], 'date': parts[4], 'buy_url': parts[5]
    }
    return render_template('ticket.html', ticket=ticket)

if __name__ == '__main__':
    app.run(debug=True)
