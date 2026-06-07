CREATE TABLE IF NOT EXISTS gold_stock_prices (
    ticker STRING,
    start_date DATE,
    end_date DATE,
    start_price DOUBLE,
    end_price DOUBLE,
    total_return DOUBLE,
    average_daily_return DOUBLE,
    volatility DOUBLE,
    average_volume DOUBLE,
    average_dollar_volume DOUBLE
)