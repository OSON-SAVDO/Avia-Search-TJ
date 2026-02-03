import requests
from flask import Flask, render_template, request

app = Flask(__name__)

TOKEN = "71876b59812fee6e1539f9365e6a12dd" # Маркератонро фаромӯш накунед
MARKER = "701004"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    orig = request.form.get('from').upper()
    dest = request.form.get('to').upper()
    url = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {"origin": orig, "destination": dest, "currency": "rub", "token": TOKEN}
    res = requests.get(url, params=params).json()
    return render_template('results.html', flights=res.get('data', []), from_n=orig, to_n=dest)

@app.route('/details')
def details():
    return render_template('details.html', f=request.args, marker=MARKER)

if __name__ == '__main__':
    app.run(debug=True)
