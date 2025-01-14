const worldData = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Türkiye",
                "code": "TUR"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [26.0433, 41.0342],
                        [26.0433, 41.0342],
                        [26.0433, 41.0342],
                        [26.0433, 41.0342],
                        [26.0433, 41.0342]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Almanya",
                "code": "DEU"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [9.921906, 54.983104],
                        [9.921906, 54.983104],
                        [9.921906, 54.983104],
                        [9.921906, 54.983104],
                        [9.921906, 54.983104]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Fransa",
                "code": "FRA"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [2.378, 48.8566],
                        [2.378, 48.8566],
                        [2.378, 48.8566],
                        [2.378, 48.8566],
                        [2.378, 48.8566]
                    ]
                ]
            }
        }
        // Diğer ülkeler buraya eklenecek...
    ]
};

// Ülke renklerini tanımla
const countryColors = {
    'TUR': '#ff4444',
    'DEU': '#44ff44',
    'FRA': '#4444ff'
    // Diğer ülke renkleri...
};

// Ülke verilerini dışa aktar
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { worldData, countryColors };
}