import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# МАЪЛУМОТИ ШУМО
TOKEN = "71876b59812fee6e1539f9365e6a12dd" 
MARKER = "701004"

def get_flights(origin, destination, date=None):
    # API барои гирифтани чиптаҳои ҳақиқӣ бо тафсилот
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_at": date,
        "currency": "tjs",
        "sorting": "price",
        "direct": "false",
        "limit": 10,
        "token": TOKEN
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get('data', [])
    except:
        return []

@app.route('/')
def index():
    return render_template('index.html', flights=[])

@app.route('/search', methods=['POST'])
def search():
    from_city = request.form.get('from', 'DYU')
    to_city = request.form.get('to', 'MOW')
    date = request.form.get('date')
    
    # Дар ин ҷо мо метавонем луғати шаҳрҳоро илова кунем ё коди IATA талаб кунем
    flights = get_flights(from_city, to_city, date)
    return render_template('index.html', flights=flights, marker=MARKER)

if __name__ == '__main__':
    app.run(debug=True)
