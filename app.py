import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# МАЪЛУМОТИ ШАХСИИ ХУДРО ИНҶО ГУЗОРЕД
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'
MARKER = '701004'

def get_iata_code(city_input):
    city_input = city_input.strip().upper()
    if len(city_input) == 3 and city_input.isalpha():
        return city_input
    try:
        url = f"https://autocomplete.travelpayouts.com/japi/bins/autocomplete?term={city_input}&locale=ru&types[]=city"
        response = requests.get(url)
        data = response.json()
        if data:
            return data[0]['code']
    except:
        return None
    return None

@app.route('/')
def index():
    return render_template('index.html', flights=None)

@app.route('/search', methods=['POST'])
def search():
    from_city = request.form.get('from', '').strip()
    to_city = request.form.get('to', '').strip()
    
    origin = get_iata_code(from_city)
    destination = get_iata_code(to_city)
    
    if not origin or not destination:
        return render_template('index.html', flights=[], error="Шаҳр ёфт нашуд.")

    # API-и мукаммалтар барои гирифтани ҷузъиёти парвоз
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
            
            for key, f in results.items():
                # Муайян кардани мустақим ё бо таваққуф (transfers)
                is_direct = "Мустақим (Прямой)" if f.get('transfers') == 0 else f"Таваққуф: {f.get('transfers')}"
                
                # Сохтани линки харид
                date_str = f['departure_at']
                search_url = f"https://www.aviasales.tj/search/{origin}{date_str[8:10]}{date_str[5:7]}{destination}1?marker={MARKER}"
                
                flights_list.append({
                    'airline': f.get('airline'),
                    'price': f.get('price'),
                    'date': date_str,
                    'type': is_direct,
                    'from_city': from_city.capitalize(),
                    'to_city': to_city.capitalize(),
                    'destination_airport': destination, # Коди фурудгоҳ
                    'buy_url': search_url
                })
        
        return render_template('index.html', flights=flights_list, searched=True)
    except Exception as e:
        return f"Хатогӣ: {e}"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
