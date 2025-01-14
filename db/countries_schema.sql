CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3), -- ISO ülke kodu (örn: TUR, USA)
    country_name VARCHAR(255),
    data_value DECIMAL(15,2), -- veya sizin veri tipiniz
    year INTEGER,
    additional_info JSON -- ek bilgiler için
); 