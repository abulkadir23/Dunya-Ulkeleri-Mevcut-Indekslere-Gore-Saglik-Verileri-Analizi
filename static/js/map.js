class MapManager {
    constructor() {
        this.initMap();
    }

    async initMap() {
        try {
            const response = await fetch('/api/map-data/');
            const visitedCountries = await response.json();
            
            // Haritayı ziyaret edilen ülkelere göre güncelle
            this.updateMapVisuals(visitedCountries);
        } catch (error) {
            console.error('Harita verileri yüklenirken hata:', error);
        }
    }

    async updateCountryVisit(countryCode, visitData) {
        try {
            const formData = new FormData();
            formData.append('country_code', countryCode);
            Object.keys(visitData).forEach(key => {
                formData.append(key, visitData[key]);
            });

            const response = await fetch('/api/update-country/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (response.ok) {
                // Haritayı güncelle
                this.updateMapVisuals({[countryCode]: visitData});
            }
        } catch (error) {
            console.error('Ülke güncellenirken hata:', error);
        }
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Kullanımı
const mapManager = new MapManager(); 