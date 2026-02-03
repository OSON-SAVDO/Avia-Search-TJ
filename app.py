from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

# Луғати тарҷумаҳо
translations = {
    'tg': {
        'title': 'Aviasales TJ - Ҷустуҷӯи чиптаҳо',
        'from': 'Аз куҷо?',
        'to': 'Ба куҷо?',
        'date': 'Санаи парвоз',
        'adults': 'Калонсолон',
        'children': 'Кӯдакон (то 12)',
        'search_btn': 'ҶУСТУҶӮИ ЧИПТА',
        'no_results': 'Чиптаҳо ёфт нашуданд.',
        'placeholder_from': 'Масалан: Душанбе',
        'placeholder_to': 'Масалан: Москва'
    },
    'ru': {
        'title': 'Aviasales TJ - Поиск билетов',
        'from': 'Откуда?',
        'to': 'Куда?',
        'date': 'Дата вылета',
        'adults': 'Взрослые',
        'children': 'Дети (до 12)',
        'search_btn': 'НАЙТИ БИЛЕТЫ',
        'no_results': 'Билеты не найдены.',
        'placeholder_from': 'Например: Душанбе',
        'placeholder_to': 'Например: Москва'
    }
}

flights_data = [
    {"from": "Душанбе", "to": "Москва", "price": 2500, "date": "2026-02-10"},
    {"from": "Душанбе", "to": "Истанбул", "price": 4200, "date": "2026-02-11"},
    {"from": "Хуҷанд", "to": "Тошканд", "price": 850, "date": "2026-02-12"}
]

@app.route('/')
def home():
    # 1. Аввал мебинем, ки оё дар URL забон ҳаст (?lang=ru)
    lang = request.args.get('lang')
    
    # 2. Агар дар URL набошад, аз Cookies мегирем
    if not lang:
        lang = request.cookies.get('language', 'tg') # 'tg' - пешфарз
    
    # Сохтани ҷавоб (Response)
    response = make_response(render_template('index.html', flights=flights_data, t=translations[lang], lang=lang))
    
    # 3. Забонро дар Cookies барои 30 рӯз захира мекунем
    response.set_cookie('language', lang, max_age=60*60*24*30)
    return response

@app.route('/search', methods=['POST'])
def search():
    # Забонро аз Cookies мегирем, то дар ҷустуҷӯ ҳам дуруст бошад
    lang = request.cookies.get('language', 'tg')
    
    start = request.form.get('from', '').strip().capitalize()
    end = request.form.get('to', '').strip().capitalize()
    
    results = [f for f in flights_data if start in f['from'] and end in f['to']]
    
    return render_template('index.html', flights=results, t=translations[lang], lang=lang)

if __name__ == '__main__':
    app.run(debug=False)
