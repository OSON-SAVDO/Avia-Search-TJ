const express = require('express');
const axios = require('axios');
const mongoose = require('mongoose');
const cors = require('cors');
const cron = require('node-cron');

const app = express();
app.use(express.json());
app.use(cors());

mongoose.connect('mongodb://localhost:27017/avia_app');

const UserSchema = new mongoose.Schema({
    email: String,
    favorites: Array,
    priceAlerts: [{
        origin: String,
        destination: String,
        targetPrice: Number
    }]
});
const User = mongoose.model('User', UserSchema);

const API_KEY = '71876b59812fee6e1539f9365e6a12dd';

app.post('/api/search', async (req, res) => {
    const { origin, destination, departDate, returnDate, adults, children, infants } = req.body;
    try {
        const response = await axios.get(`https://api.travelpayouts.com/v2/prices/latest`, {
            params: {
                origin, destination, depart_date: departDate, return_date: returnDate,
                adults, children, infants, token: API_KEY, currency: 'USD'
            }
        });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/alerts', async (req, res) => {
    const { email, alert } = req.body;
    await User.findOneAndUpdate({ email }, { $push: { priceAlerts: alert } }, { upsert: true });
    res.sendStatus(200);
});

cron.schedule('0 0 * * *', async () => {
    const alerts = await User.find({});
    // Logic for checking prices and sending notifications
});

app.listen(3000);
