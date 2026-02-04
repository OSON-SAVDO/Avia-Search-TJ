const API_TOKEN = '71876b59812fee6e1539f9365e6a12dd';
const MARKER = '701004';

let currentTickets = [];

document.getElementById('searchBtn').addEventListener('click', async () => {
    const origin = document.getElementById('origin').value.toUpperCase();
    const destination = document.getElementById('destination').value.toUpperCase();
    const date = document.getElementById('departDate').value;

    if (!origin || !destination || !date) {
        alert("Лутфан тамоми майдонҳоро пур кунед!");
        return;
    }

    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('resultsList').innerHTML = '';

    const url = `https://api.travelpayouts.com/v2/prices/latest?origin=${origin}&destination=${destination}&beginning_of_period=${date}&token=${API_TOKEN}&currency=usd&limit=50`;

    try {
        const response = await fetch(url);
        const result = await response.json();
        
        if (result.success && result.data.length > 0) {
            currentTickets = result.data;
            renderTickets(currentTickets);
            document.getElementById('filtersArea').style.display = 'flex';
        } else {
            document.getElementById('resultsList').innerHTML = '<p style="text-align:center;">Чипта ёфт нашуд.</p>';
        }
    } catch (error) {
        alert("Хатогӣ ҳангоми пайвастшавӣ ба API");
    } finally {
        document.getElementById('loader').classList.add('hidden');
    }
});

function renderTickets(tickets) {
    const container = document.getElementById('resultsList');
    container.innerHTML = '';

    tickets.forEach(t => {
        const card = document.createElement('div');
        card.className = 'ticket-card';
        card.innerHTML = `
            <div class="ticket-price">$${t.value}</div>
            <div class="ticket-details">
                <strong>Парвоз:</strong> ${t.origin} ✈️ ${t.destination}<br>
                <strong>Сана:</strong> ${t.depart_date}<br>
                <strong>Таваққуф:</strong> ${t.number_of_changes === 0 ? 'Бе таваққуф (Прямой)' : t.number_of_changes + ' бор'}<br>
                <strong>Ширкат/Агентӣ:</strong> ${t.gate}
            </div>
            <button class="buy-now" onclick="window.open('https://www.aviasales.com${t.link}?marker=${MARKER}')">ХАРИДАН ВА ПАРДОХТ</button>
        `;
        container.appendChild(card);
    });
}

function sortTickets(type) {
    if(type === 'price') {
        currentTickets.sort((a, b) => a.value - b.value);
        renderTickets(currentTickets);
    }
}

function filterDirect() {
    const direct = currentTickets.filter(t => t.number_of_changes === 0);
    renderTickets(direct);
}

function showPriceMap() {
    window.open(`https://map.aviasales.com/?origin=${document.getElementById('origin').value}`, '_blank');
}
