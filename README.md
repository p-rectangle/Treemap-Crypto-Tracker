# Treemap-Crypto-Tracker
This crypto tracker uses a CSV file to track crypto in an easy to see treemap format.

This script uses the binance trading pairs where USDT is used to track the token.

symbol,amount,USD_Purchase_Value,Purchase_Price

AAVEUSDT,0.59946,94.62,0

USD_Purchase_Value 
  This is the total you've spent buying a crypto, say $10 + $20 + $50 = $80 over a few months etc

Purchase_Price
  This is the one time price you've bought it for

The code will use the USD_Purchase_Value first but default to the Purcahse_Price if it's not present. 
Use the USD_Purchase_Value if possible.
