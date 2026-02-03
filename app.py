import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# САТРҲОИ 8 ва 9: МАЪЛУМОТИ API-И ХУДРО ИНҶО ГУЗОРЕД
TOKEN = "<script data-noptimize="1" data-cfasync="false" data-wpfc-render="false">
  (function () {
      var script = document.createElement("script");
      script.async = 1;
      script.src = 'https://emrldco.com/NDk1MDAx.js?t=495001';
      document.head.appendChild(script);
  })();
</script>"  # Аз Travelpayouts гиред
MARKER = ""    # Аз Travelpayouts гиред

# Луғати кодҳои шаҳрҳо (IATA)
CITY_CODES = {
    "Душанбе": "DYU", "Хуҷанд": "LBD", "Москва": "MOW", 
    "Санкт-Петербург": "LED", "Истанбул": "IST", "Дубай": "DXB"
}

def get_real_flights(origin, destination, date=None):
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {
        "origin": origin, "destination": destination,
        "departure_at": date, "currency": "tjs",
        "sorting": "price", "direct": "false",
        "limit": 10, "token": TOKEN
    }
    try:
        response = requests.get(url, params=params)
        return response.json().get('data', [])
    except:
        return []

@app.route('/')
def index():
    return render_template('index.html', flights=[])

@app.route('/search', methods=['POST'])
def search():
    from_city = request.form.get('from', 'Душанбе')
    to_city = request.form.get('to', 'Москва')
    date = request.form.get('departure_date')
    
    # Табдил додани номи шаҳр ба код (масалан: Душанбе -> DYU)
    origin = CITY_CODES.get(from_city, "DYU")
    dest = CITY_CODES.get(to_city, "MOW")
    
    flights = get_real_flights(origin, dest, date)
    return render_template('index.html', flights=flights, marker=MARKER)

if __name__ == '__main__':
    app.run(debug=True)
