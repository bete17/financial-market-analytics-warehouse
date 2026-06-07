CREATE TABLE IF NOT EXISTS silver_stock_prices (
    date DATE,
    ticker STRING,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    adj_close DOUBLE,
    volume BIGINT,
    daily_return DOUBLE,
    daily_volume DOUBLE, 
)