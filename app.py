import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- МАЪЛУМОТИ ХУДРО ИНҶО ГУЗОРЕД ---
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'
MARKER = '701004'
# ----------------------------------

@app.route('/')
def index():
    return render_template('index.html', flights=None)

@app.route('/search', methods=['POST'])
def search():
    # Мо кодҳои IATA-ро аз hidden input-ҳо мегирем
    origin = request.form.get('from') 
    destination = request.form.get('to')
    
    # Номҳои шаҳрҳо барои зебоӣ дар экран
    from_name = request.form.get('from_display', 'Душанбе')
    to_name = request.form.get('to_display', 'Москва')

    # Агар корбар аз рӯйхат интихоб накарда бошад, кӯшиш мекунем кодро худамон ёбем
    if not origin or len(origin) != 3:
        return render_template('index.html', error="Лутфан шаҳрро аз рӯйхати пайдошуда интихоб кунед.")

    # Дархост ба API-и Aviasales
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
                date_str = f['departure_at']
                # Формулаи линки харид бо Маркери шумо
                buy_url = f"https://www.aviasales.tj/search/{origin}{date_str[8:10]}{date_str[5:7]}{destination}1?marker={MARKER}"
                
                flights_list.append({
                    'airline': f.get('airline'),
                    'price': f.get('price'),
                    'date': date_str[:10],
                    'type': "Мустақим" if f.get('transfers') == 0 else f"Таваққуф: {f.get('transfers')}",
                    'from_city': from_name,
                    'to_city': to_name,
                    'origin_code': origin,
                    'destination_code': destination,
                    'buy_url': buy_url
                })
        
        return render_template('index.html', flights=flights_list, searched=True)
    except Exception as e:
        return f"Хатогии сервер: {e}"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
