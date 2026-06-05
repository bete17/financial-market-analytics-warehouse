# Version 1 Plan

## Objective

Build the first version of a financial market analytics warehouse using historical stock price data.

## Version 1 Pipeline

Raw CSV files  
→ Bronze layer  
→ Silver layer  
→ Gold analytics tables

## Bronze Layer

The bronze layer stores raw stock price data.

Expected columns:

- date
- ticker
- open
- high
- low
- close
- adj_close
- volume
- source_file
- loaded_at

## Silver Layer

The silver layer stores cleaned stock price data.

Transformations:

- Standardize column names
- Convert date column to date format
- Convert price and volume columns to numeric values
- Remove duplicate rows
- Sort records by ticker and date
- Calculate daily return
- Calculate dollar volume

## Gold Layer

The gold layer stores analytics-ready tables.

Planned gold tables:

- gold_stock_performance_summary
- gold_moving_averages
- gold_volume_summary

## Metrics

Version 1 will calculate:

- Daily return
- Total return
- Average daily return
- Volatility
- 20-day moving average
- 50-day moving average
- Average trading volume
- Average dollar volume

## Success Criteria

Version 1 is complete when:

- Raw stock data can be loaded
- Cleaned silver data can be created
- Gold summary tables can be generated
- The project has clear documentation
- All code is version-controlled on GitHub
