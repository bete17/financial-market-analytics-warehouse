CREATE TABLE IF NOT EXISTS bronze_stock_prices (
    date DATE,
    ticker STRING,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    adj_close DOUBLE,
    volume BIGINT,
    source_file STRING,
    loaded_at TIMESTAMP
);

-- loaded_at : time stamp of when the data was loaded into the table
-- adj_close : adjusted close price, which accounts for corporate actions 
--             like dividends and stock stocks-splits