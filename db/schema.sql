CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE map_data (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    data_type VARCHAR(50),
    value JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 