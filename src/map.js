const db = require('../utils/DatabaseHelper');

async function initializeMapAndTable() {
  try {
    // Tüm ülke verilerini çek
    const countriesData = await db.getAllCountriesData();
    
    // Haritayı güncelle
    countriesData.forEach(country => {
      // Haritada ülkeyi vurgula
      highlightCountry(country.country_code, {
        value: country.data_value,
        color: getColorBasedOnValue(country.data_value)
      });
    });

    // Tabloyu güncelle
    updateDataTable(countriesData);
    
  } catch (error) {
    console.error('Veri yükleme hatası:', error);
  }
}

function updateDataTable(data) {
  const tableBody = document.querySelector('#dataTable tbody');
  tableBody.innerHTML = '';

  data.forEach(country => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${country.country_name}</td>
      <td>${country.data_value}</td>
      <td>${country.year}</td>
      <td>${formatAdditionalInfo(country.additional_info)}</td>
    `;
    
    // Tablo satırına tıklandığında haritada ilgili ülkeyi vurgula
    row.addEventListener('click', () => {
      zoomToCountry(country.country_code);
    });

    tableBody.appendChild(row);
  });
}

// Ülke koduna göre haritada yakınlaştırma
function zoomToCountry(countryCode) {
  // Harita API'nize göre uyarlayın
  map.setFocus(countryCode);
}

// Değere göre renk belirleme
function getColorBasedOnValue(value) {
  // Değer aralıklarına göre renk döndür
  if (value > 1000) return '#ff0000';
  if (value > 500) return '#ffff00';
  return '#00ff00';
} 