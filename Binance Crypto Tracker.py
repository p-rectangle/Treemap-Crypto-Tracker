import requests
import pandas as pd
import plotly.express as px
import numpy as np

# Binance API endpoint for ticker prices (public)
binance_api_url = "https://api.binance.com/api/v3/ticker/price"

# Read the portfolio from the CSV file
portfolio_df = pd.read_csv('Binance.csv')

# Fetch real-time prices from Binance (public API)
prices = {}
for index, row in portfolio_df.iterrows():
    symbol = row['symbol']
    response = requests.get(binance_api_url, params={'symbol': symbol})
    
    try:
        data = response.json()
        prices[symbol] = float(data['price'])
    except KeyError as e:
        print(f"Error fetching price for {symbol}. Response: {response.text}")
        prices[symbol] = None

# Filter out symbols with missing prices
portfolio_df = portfolio_df[portfolio_df['symbol'].isin(prices.keys())]

# Calculate the total value of each cryptocurrency in the portfolio
portfolio_df['value'] = round((portfolio_df['amount'] * portfolio_df['symbol'].map(prices)), 2)

# Calculate the PurchaseCost based on 'Purchase_Price' or 'USD_Purchase_Value'
portfolio_df["PurchaseCost"] = np.where(portfolio_df['Purchase_Price'] == 0, round(portfolio_df['USD_Purchase_Value'], 2),
                                        round((portfolio_df['amount'] * portfolio_df['Purchase_Price']), 2))

# Calculate the percentage change, handling division by zero
#portfolio_df["PercentageChange"] = np.where(portfolio_df['Purchase_Price'] == 0, 0,
#                                             round((portfolio_df['symbol'].map(prices) / portfolio_df["Purchase_Price"]) * 100 - 100, 2))

portfolio_df["PercentageChange"] = round((portfolio_df['value'] / portfolio_df["PurchaseCost"]) * 100 - 100, 2)


# Calculate the total value of the portfolio
total_portfolio_value = portfolio_df['value'].sum()
portfolio_cost = portfolio_df['PurchaseCost'].sum()
portfolio_percentage = round((total_portfolio_value / portfolio_cost - 1) * 100, 2)

# Create a treemap with a dummy parent symbol
portfolio_df['parent'] = 'All Cryptocurrencies'
fig = px.treemap(
    names=portfolio_df['symbol'],
    parents=portfolio_df['parent'],
    values=portfolio_df['value'],
    title=f"Crypto Portfolio Treemap (Current Value: {total_portfolio_value:.2f} USD {portfolio_percentage}%)",
    color=portfolio_df['value'],
    color_continuous_scale='Viridis'
)

fig.data[0].customdata = np.column_stack([portfolio_df['symbol'], portfolio_df['value'], portfolio_df["PurchaseCost"], portfolio_df["PercentageChange"]])
fig.data[0].texttemplate = "%{customdata[0]}<br>Current Value: $%{customdata[1]}<br>Purchase Value: $%{customdata[2]}<br>Percentage Change: %{customdata[3]}%"

# Show the treemap
fig.show()
