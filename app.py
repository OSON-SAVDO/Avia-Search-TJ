import requests
from flask import Flask, render_template, request

app = Flask(__name__)

TOKEN = "71876b59812fee6e1539f9365e6a12dd" 
MARKER = "701004"

# Функсия барои табдили номи шаҳр ба код (Тюмень -> TJM)
def get_city_code(city_name):
    url = f"https://autocomplete.travelpayouts.com/places2?term={city_name}&locale=ru&types[]=city"
    try:
        res = requests.get(url).json()
        return res[0]['code'] if res else city_name.upper()
    except:
        return city_name.upper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    from_city_name = request.form.get('from')
    to_city_name = request.form.get('to')
    
    origin = get_city_code(from_city_name)
    destination = get_city_code(to_city_name)
    
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {
        "origin": origin,
        "destination": destination,
        "currency": "rub",
        "token": TOKEN,
        "sorting": "price",
        "limit": 15
    }
    
    res = requests.get(url, params=params).json()
    flights = res.get('data', [])
    
    return render_template('results.html', flights=flights, from_n=from_city_name, to_n=to_city_name)

@app.route('/details')
def details():
    return render_template('details.html', f=request.args, marker=MARKER)

if __name__ == '__main__':
    app.run(debug=True)
