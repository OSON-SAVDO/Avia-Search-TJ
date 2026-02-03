import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

TOKEN = "71876b59812fee6e1539f9365e6a12dd" # Маркер: 701004
MARKER = "701004"

# Функсия барои ёфтани кодҳои IATA (масалан Москва -> MOW, SVO, DME)
def get_iata_code(query):
    url = f"https://autocomplete.travelpayouts.com/places2?term={query}&locale=ru&types[]=city&types[]=airport"
    try:
        res = requests.get(url).json()
        return res[0]['code'] if res else query.upper()
    except:
        return query.upper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    from_city = request.form.get('from')
    to_city = request.form.get('to')
    date = request.form.get('date')

    # Табдили номи шаҳр ба код (масалан Москва -> MOW)
    origin = get_iata_code(from_city)
    destination = get_iata_code(to_city)

    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_at": date,
        "unique": "false", # Барои он ки тамоми фурудгоҳҳоро нишон диҳад
        "sorting": "price",
        "token": TOKEN,
        "currency": "rub"
    }
    
    response = requests.get(url, params=params).json()
    flights = response.get('data', [])
    
    return render_template('index.html', flights=flights, from_n=from_city, to_n=to_city)

if __name__ == '__main__':
    app.run(debug=True)
