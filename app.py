import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# МАЪЛУМОТИ ШАХСИИ ХУДРО ИНҶО ГУЗОРЕД
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'
MARKER = '701004'

# --- РӮЙХАТИ ШАҲРҲО ВА ФУРУДГОҲҲО (ИНҶОРО ХУДАШОН ПУР КУНЕД) ---
AIRPORTS_DB = {
    "ДУШАНБЕ": "DYU",
    "МОСКВА": "MOW",
    "ХУҶАНД": "LBD",
    "ИСТАНБУЛ": "IST",
    "АЛМАТЫ": "ALA",
    "ТОШКЕНТ": "TAS",
    "ДУБАЙ": "DXB",
    "САНКТ-ПЕТЕРБУРГ": "LED",
    "КУЛОБ": "TJU",
    "БОХТАР": "KQT",
    "ЛОНДОН": "LON",
    "ПАРИЖ": "PAR",
    "САНКТ-ПЕТЕРБУРГ: "LED", 
    "​ЕКАТЕРИНБУРГ: "SVX", 
    "​НОВОСИБИРСК: "OVB", 
    "​ҚАЗОН: "KZN", 
    "​КРАСНОДАР: "KRR", 
    "​УФА: "UFA", 
    "​СОЧИ: "AER", 
    "​САМАРА: "KUF", 
    "​ЧЕЛЯБИНСК: "CEK", 
    "​РОСТОВ-НА-ДОНУ: "ROV", 
    "​КРАСНОЯРСК: "KJA", 
    "​ИРКУТСК: "IKT", 
    "​ТЮМЕНЬ: "TJM", 
    "​СУРГУТ: "SGC", 
    "​НИЖНИЙ НОВГОРОД: "GOJ", 
    "​ОМСК: "OMS
    "​ОРЕНБУРГ: "REN", 
    "​ВОЛГОГРАД: "VOG", 
​    "МИФИ: "MCX", 
    # Шумо метавонед инҷо сатрҳои нав илова кунед: "НОМИ ШАҲР": "КОДИ IATA"
}

@app.route('/')
def index():
    return render_template('index.html', flights=None)

@app.route('/search', methods=['POST'])
def search():
    # Гирифтани номҳо аз форма ва табдил ба ҳарфҳои калон
    from_city_name = request.form.get('from_display', '').strip().upper()
    to_city_name = request.form.get('to_display', '').strip().upper()
    
    # Ёфтани кодҳо аз базаи мо
    origin = AIRPORTS_DB.get(from_city_name)
    destination = AIRPORTS_DB.get(to_city_name)

    if not origin or not destination:
        return render_template('index.html', 
                               error=f"Шаҳр ёфт нашуд. Танҳо шаҳрҳои дар база бударо нависед.")

    # API-и мукаммалтар (v3) барои ёфтани чиптаҳои бештар
    url = "https://api.travelpayouts.com/v3/prices_for_dates"
    params = {
        'origin': origin,
        'destination': destination,
        'token': API_TOKEN,
        'currency': 'tjs',
        'unique': 'true',
        'limit': 10
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        flights_list = []
        if data.get('success') and 'data' in data:
            for f in data['data']:
                date_str = f.get('departure_at', '')
                # Сохтани линк барои харид
                buy_url = f"https://www.aviasales.tj/search/{origin}{date_str[8:10]}{date_str[5:7]}{destination}1?marker={MARKER}"
                
                flights_list.append({
                    'airline': f.get('airline'),
                    'price': f.get('price'),
                    'date': date_str[:10],
                    'type': "Мустақим" if f.get('transfers') == 0 else f"Таваққуф: {f.get('transfers')}",
                    'from_city': from_city_name.capitalize(),
                    'to_city': to_city_name.capitalize(),
                    'origin_code': origin,
                    'destination_code': destination,
                    'buy_url': buy_url
                })
        
        if not flights_list:
            return render_template('index.html', error="Дар ин масир чипта ёфт нашуд.")

        return render_template('index.html', flights=flights_list)

    except Exception as e:
        return f"Хатогии пайвастшавӣ: {e}"

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
