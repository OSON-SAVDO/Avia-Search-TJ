import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- МАЪЛУМОТИ ШАХСИИ ХУДРО ИНҶО ГУЗОРЕД ---
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'
MARKER = '701004'
# ------------------------------------------

def get_iata_code(city_input):
    """
    Ин функсия номи шаҳрро мегирад ва коди 3-ҳарфаи IATA-ро меёбад.
    Агар корбар аллакай код навишта бошад (масалан: DYU), онро мустақим истифода мебарад.
    """
    city_input = city_input.strip().upper()
    
    # Агар воридот аллакай коди 3-ҳарфа бошад
    if len(city_input) == 3 and city_input.isalpha():
        return city_input
    
    # Ҷустуҷӯи коди IATA тавассути Autocomplete API
    try:
        # Мо 'locale=ru'-ро истифода мебарем, то номҳои кириллицаро беҳтар фаҳмад
        url = f"https://autocomplete.travelpayouts.com/japi/bins/autocomplete?term={city_input}&locale=ru&types[]=city"
        response = requests.get(url)
        data = response.json()
        if data and len(data) > 0:
            return data[0]['code']
    except Exception as e:
        print(f"Хатогӣ дар Autocomplete: {e}")
        return None
    return None

@app.route('/')
def index():
    # Саҳифаи асосӣ бидуни натиҷаҳои ҷустуҷӯ
    return render_template('index.html', flights=None)

@app.route('/search', methods=['POST'])
def search():
    from_city_name = request.form.get('from', '').strip()
    to_city_name = request.form.get('to', '').strip()
    
    # 1. Табдил додани номҳо ба кодҳои IATA
    origin = get_iata_code(from_city_name)
    destination = get_iata_code(to_city_name)
    
    # Агар шаҳрҳо ёфт нашаванд, хатогиро нишон медиҳем
    if not origin or not destination:
        return render_template('index.html', 
                               flights=[], 
                               error="Шаҳр ёфт нашуд. Лутфан номро дуруст нависед (масалан: Душанбе).")

    # 2. Дархост ба API-и Aviasales барои гирифтани нархҳо
    url = "https://api.travelpayouts.com/v1/prices/cheap"
    params = {
        'origin': origin,
        'destination': destination,
        'token': API_TOKEN,
        'currency': 'tjs' # Нархҳо бо сомонӣ
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
                
                # Сохтани линки шарикӣ бо Маркери шумо барои гирифтани фоида
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
        return f"Хатогии техникӣ ҳангоми дархости чиптаҳо: {e}"

@app.route('/ticket/<path:info>')
def ticket_details(info):
    """
    Саҳифаи тафсилоти чипта, ки маълумотро аз URL мегирад.
    """
    try:
        parts = info.split('|')
        ticket = {
            'airline': parts[0],
            'price': parts[1],
            'from_city': parts[2],
            'to_city': parts[3],
            'date': parts[4],
            'buy_url': parts[5]
        }
        return render_template('ticket.html', ticket=ticket)
    except:
        return "Хатогӣ дар намоиши тафсилот", 400

if __name__ == '__main__':
    # Барои Render ва дигар хостингҳо портро муайян мекунем
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
