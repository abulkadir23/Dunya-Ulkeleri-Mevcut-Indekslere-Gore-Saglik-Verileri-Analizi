const config = {
  development: {
    host: 'localhost',
    database: 'son_veriler2',
    user: 'postgres',
    password: 'şifreniz',
    port: 5432
  },
  production: {
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT
  }
};

module.exports = config; 