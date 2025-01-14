const { Pool } = require('pg');
const config = require('../config/database');

class DatabaseHelper {
  constructor() {
    this.pool = new Pool(config[process.env.NODE_ENV || 'development']);
  }

  async getLocations() {
    const query = 'SELECT * FROM locations';
    const result = await this.pool.query(query);
    return result.rows;
  }

  async addLocation(name, latitude, longitude, description) {
    const query = `
      INSERT INTO locations (name, latitude, longitude, description)
      VALUES ($1, $2, $3, $4)
      RETURNING *
    `;
    const values = [name, latitude, longitude, description];
    const result = await this.pool.query(query, values);
    return result.rows[0];
  }

  async getMapData(locationId) {
    const query = 'SELECT * FROM map_data WHERE location_id = $1';
    const result = await this.pool.query(query, [locationId]);
    return result.rows;
  }

  async getCountryData(countryCode) {
    const query = 'SELECT * FROM countries WHERE country_code = $1';
    const result = await this.pool.query(query, [countryCode]);
    return result.rows[0];
  }

  async getAllCountriesData() {
    const query = `
      SELECT 
        "Country" as country_name,
        "Life expectancy(years) (Country)" as life_expectancy,
        "Happiness levels(Country" as happiness_level,
        "Cost of Living Index" as cost_of_living,
        "Local Purchasing Power Index" as purchasing_power,
        "Obesity levels(Country)" as obesity_level,
        "Annual avg. hours worked" as annual_work_hours
      FROM son_veriler2
      GROUP BY "Country"
    `;
    const result = await this.pool.query(query);
    return result.rows;
  }

  async getCountryDataByYear(year) {
    const query = 'SELECT * FROM countries WHERE year = $1';
    const result = await this.pool.query(query, [year]);
    return result.rows;
  }

  async getCountryDetails(countryName) {
    const query = `
      SELECT 
        "City",
        "Pollution(Index score) (City)" as pollution,
        "Sunshine hours(City)" as sunshine_hours,
        "Outdoor activities(City)" as outdoor_activities,
        "Number of take out places(City)" as takeout_places,
        "Cost of a monthly gym membership(City)" as gym_cost,
        "Cost of a bottle of water(City)" as water_cost
      FROM son_veriler2
      WHERE "Country" = $1
    `;
    const result = await this.pool.query(query, [countryName]);
    return result.rows;
  }
}

module.exports = new DatabaseHelper(); 