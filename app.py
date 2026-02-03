import requests
from flask import Flask, render_template, request

app = Flask(__name__)

TOKEN = "71876b59812fee6e1539f9365e6a12dd"
MARKER = "701004"

@app.route('/')
def index():
    # Қадами 1: Саҳифаи асосии ҷустуҷӯ (Акси 5899)
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Қадами 2: Намоиши рӯйхати чиптаҳо (Акси 5922)
    from_city = request.form.get('from').upper()
    to_city = request.form.get('to').upper()
    
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {"origin": from_city, "destination": to_city, "currency": "rub", "token": TOKEN}
    
    res = requests.get(url, params=params).json()
    flights = res.get('data', [])
    return render_template('results.html', flights=flights, from_n=from_city, to_n=to_city)

@app.route('/ticket_details')
def ticket_details():
    # Қадами 3: Саҳифаи тафсилот (Акси 5920)
    data = request.args
    return render_template('details.html', f=data, marker=MARKER)

if __name__ == '__main__':
    app.run(debug=True)
