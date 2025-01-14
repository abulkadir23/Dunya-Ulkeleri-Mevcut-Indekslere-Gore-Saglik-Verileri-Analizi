const express = require('express');
const path = require('path');
const app = express();

// Statik dosyaları serve et
app.use('/static', express.static('static'));

// Ana sayfayı serve et
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API endpoint'i
app.get('/api/countries', async (req, res) => {
    try {
        const db = require('./utils/DatabaseHelper');
        const data = await db.getAllCountriesData();
        res.json(data);
    } catch (error) {
        console.error('API Hatası:', error);
        res.status(500).json({ error: error.message });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Sunucu http://localhost:${PORT} adresinde çalışıyor`);
}); 