# Stock Research Terminal for cs50p

A small Python project I built as my final project for **CS50's Introduction to Programming with Python (CS50P)**.

The goal was to build a simple stock research tool that goes a bit further than just looking at a stock's price. The program downloads historical market data and uses it to calculate basic performance and risk measures.

## What it does

The user enters:

* A stock ticker
* A benchmark ticker
* A start date
* An end date

The program calculates then several statistics including:

* Total return
* Daily returns
* Mean and median daily returns
* CAGR (Compound Annual Growth Rate)
* Variance and standard deviation
* Annualized volatility
* Covariance and correlation with the benchmark
* Sharpe ratio
* Beta
* Alpha based on the CAPM framework

It also creates three simple charts:

* Daily returns
* Normalized performance (starting at 100)
* Distribution of daily returns

The 10-year US Treasury yield (`^TNX`) is used as the risk-free rate for the Sharpe ratio and alpha calculations.

## Why I built it

I am interested in financial markets, so I wanted my final CS50P project to be linked to something I actually wanted to understand better.

The main purpose of the project was not to build a professional trading system, but to practice Python by applying it to financial data.

## How to use it

Run:

```bash
python project.py
```

The program will ask for the stock ticker, benchmark, start date and end date.

For example:

```text
Stock ticker: AAPL
Benchmark ticker: ^GSPC
Start date: 2020-01-01
End date: 2025-01-01
```

The program downloads then the required data and displays the calculations and charts.

## Project structure

### `project.py`

Contains the main program and the functions used to download data, perform the calculations and generate the charts.

### `test_project.py`

Contains tests written with `pytest` for some of the main calculation functions.

### `requirements.txt`

Lists the Python libraries required to run the project.

## Libraries

The project uses:

* `yfinance` for historical market data
* `pandas` for data manipulation
* `numpy` for numerical calculations
* `matplotlib` for data visualization
* `pytest` for testing

## Testing

I used `pytest` to test some of the calculation functions with predefined data.

For example, the tests check return calculations, descriptive statistics and CAGR calculations.

To run the tests:

```bash
python -m pytest
```

`pytest.approx()` is used when necessary because some financial calculations involve floating-point numbers.

## Limitations

This is a relatively simple educational project, not a professional financial analysis platform.

The results depend on the historical data available through Yahoo Finance. The project also uses a simplified approach to the risk-free rate and does not attempt to provide investment recommendations or predict future prices.

There are also several aspects that could be improved in a future version, such as better handling of missing data, more advanced statistical analysis and a more developed user interface.
