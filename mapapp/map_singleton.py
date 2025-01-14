from typing import Dict, Optional
from django.db import connection

class WorldMapSingleton:
    _instance: Optional['WorldMapSingleton'] = None
    _map_data: Dict = {}
    _is_initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorldMapSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            self._load_map_data()
            self._is_initialized = True

    def _load_map_data(self):
        """Veritabanından harita verilerini yükler"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT country_code, country_name, visited, notes, visit_date 
                FROM mapapp_countryvisit
            """)
            rows = cursor.fetchall()
            for row in rows:
                self._map_data[row[0]] = {
                    'country_name': row[1],
                    'visited': row[2],
                    'notes': row[3],
                    'visit_date': row[4]
                }

    def get_country_data(self, country_code: str) -> Dict:
        """Belirli bir ülkenin verilerini döndürür"""
        return self._map_data.get(country_code, {})

    def update_country_data(self, country_code: str, data: Dict) -> None:
        """Ülke verilerini günceller"""
        self._map_data[country_code] = data
        # Veritabanını da güncelle
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO mapapp_countryvisit 
                (country_code, country_name, visited, notes, visit_date)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (country_code) DO UPDATE 
                SET visited = %s, notes = %s, visit_date = %s
            """, [
                country_code,
                data['country_name'],
                data['visited'],
                data['notes'],
                data['visit_date'],
                data['visited'],
                data['notes'],
                data['visit_date']
            ])

    def get_all_visited_countries(self) -> Dict:
        """Ziyaret edilmiş tüm ülkeleri döndürür"""
        return {k: v for k, v in self._map_data.items() if v.get('visited')}

    def clear_cache(self) -> None:
        """Cache'i temizler ve verileri yeniden yükler"""
        self._map_data = {}
        self._load_map_data() 