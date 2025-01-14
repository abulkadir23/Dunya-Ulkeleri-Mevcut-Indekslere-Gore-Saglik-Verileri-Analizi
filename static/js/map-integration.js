const { worldData, countryColors } = require('./world-countries');
const db = require('../../utils/DatabaseHelper');

let map;
let currentCountryData = {};

async function initializeMap() {
    try {
        console.log('Harita başlatılıyor...');
        const response = await fetch('/api/countries/');
        const data = await response.json();
        const dbCountries = data.countries;
        console.log('Veritabanından gelen veriler:', dbCountries);
        
        // Verileri ülke kodlarına göre eşleştir
        dbCountries.forEach(country => {
            currentCountryData[country.country_name] = country;
        });

        // Haritayı oluştur ve verileri göster
        renderMap();
        updateDataTable();

    } catch (error) {
        console.error('Hata:', error);
    }
}

function renderMap() {
    // Haritayı oluştur
    map = L.map('map').setView([0, 0], 2);
    
    // Her ülke için
    worldData.features.forEach(feature => {
        const countryCode = feature.properties.code;
        const countryData = currentCountryData[countryCode];
        
        // Ülke sınırlarını çiz
        L.geoJSON(feature, {
            style: () => ({
                fillColor: getColorBasedOnValue(countryData?.data_value),
                weight: 1,
                opacity: 1,
                color: 'white',
                fillOpacity: 0.7
            }),
            onEachFeature: (feature, layer) => {
                // Tıklama olayını ekle
                layer.on('click', () => {
                    highlightCountry(countryCode);
                });
                
                // Tooltip ekle
                layer.bindTooltip(`
                    <strong>${feature.properties.name}</strong>
                    ${countryData ? `
                        <br>Değer: ${countryData.data_value}
                        <br>Yıl: ${countryData.year}
                    ` : ''}
                `);
            }
        }).addTo(map);
    });
}

function updateDataTable() {
    const tableBody = document.querySelector('#dataTable tbody');
    tableBody.innerHTML = '';

    Object.values(currentCountryData).forEach(country => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${country.country_name}</td>
            <td>${formatValue(country.life_expectancy, 'yıl')}</td>
            <td>${formatValue(country.happiness_level, '/10')}</td>
            <td>${formatValue(country.cost_of_living, 'index')}</td>
            <td>${formatValue(country.purchasing_power, 'index')}</td>
        `;
        
        row.addEventListener('click', async () => {
            highlightCountry(country.country_name);
            // Ülkeye ait şehir detaylarını göster
            const cityDetails = await db.getCountryDetails(country.country_name);
            showCityDetails(cityDetails);
        });

        tableBody.appendChild(row);
    });
}

function formatValue(value, unit) {
    if (!value) return '-';
    return `${value} ${unit}`;
}

function showCityDetails(cities) {
    const detailsDiv = document.querySelector('#cityDetails');
    if (!cities.length) return;

    const html = cities.map(city => `
        <div class="city-card">
            <h3>${city.City}</h3>
            <ul>
                <li>Kirlilik Endeksi: ${city.pollution}</li>
                <li>Güneşli Saatler: ${city.sunshine_hours}</li>
                <li>Açık Hava Aktiviteleri: ${city.outdoor_activities}</li>
                <li>Paket Servis Yerleri: ${city.takeout_places}</li>
                <li>Aylık Spor Salonu Üyeliği: ${city.gym_cost}</li>
                <li>Su Şişesi Maliyeti: ${city.water_cost}</li>
            </ul>
        </div>
    `).join('');

    detailsDiv.innerHTML = html;
}

function highlightCountry(countryCode) {
    // Seçili ülkeyi vurgula
    const country = currentCountryData[countryCode];
    if (country) {
        // Haritada ülkeyi yakınlaştır
        const feature = worldData.features.find(f => f.properties.code === countryCode);
        if (feature) {
            const bounds = L.geoJSON(feature).getBounds();
            map.fitBounds(bounds);
        }
        
        // Tablodan ilgili satırı bul ve vurgula
        const rows = document.querySelectorAll('#dataTable tbody tr');
        rows.forEach(row => {
            if (row.cells[0].textContent === country.country_name) {
                row.classList.add('highlighted');
            } else {
                row.classList.remove('highlighted');
            }
        });
    }
}

function getColorBasedOnValue(value) {
    if (!value) return '#cccccc'; // Veri yoksa gri renk
    if (value > 1000) return '#ff0000';
    if (value > 500) return '#ffff00';
    return '#00ff00';
}

function formatAdditionalInfo(info) {
    if (!info) return '-';
    try {
        return Object.entries(info)
            .map(([key, value]) => `${key}: ${value}`)
            .join('<br>');
    } catch (e) {
        return '-';
    }
}

// Sayfa yüklendiğinde haritayı başlat
document.addEventListener('DOMContentLoaded', initializeMap); 