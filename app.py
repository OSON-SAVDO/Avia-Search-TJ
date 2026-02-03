import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

TOKEN = "71876b59812fee6e1539f9365e6a12dd"
MARKER = "701004"

CITY_CODES = {"душанбе": "DYU", "москва": "MOW", "стамбул": "IST", "двубай": "DXB"}

@app.route('/')
def index():
    return render_template('index.html', flights=[])

@app.route('/search', methods=['POST'])
def search():
    from_city = request.form.get('from', '').lower()
    to_city = request.form.get('to', '').lower()
    origin = CITY_CODES.get(from_city, from_city.upper())
    destination = CITY_CODES.get(to_city, to_city.upper())
    
    url = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {"origin": origin, "destination": destination, "currency": "rub", "token": TOKEN}
    
    response = requests.get(url, params=params)
    flights = response.json().get('data', [])
    
    return render_template('index.html', flights=flights, from_n=from_city.title(), to_n=to_city.title())

# САҲИФАИ ТАФСИЛОТ (Маҳз барои акси 5920)
@app.route('/details')
def details():
    price = request.args.get('price')
    airline = request.args.get('airline')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    dep_at = request.args.get('dep_at')
    
    return render_template('details.html', price=price, airline=airline, origin=origin, destination=destination, dep_at=dep_at, marker=MARKER)

if __name__ == '__main__':
    app.run(debug=True)
