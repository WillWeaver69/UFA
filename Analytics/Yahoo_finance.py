import pandas as pd
from yahoo_fin import stock_info as si
import yfinance as yf

# gather stock symbols from major US exchanges
df1 = pd.DataFrame( si.tickers_sp500() )
df2 = pd.DataFrame( si.tickers_nasdaq() )
df3 = pd.DataFrame( si.tickers_dow() )
df4 = pd.DataFrame( si.tickers_other() )

# convert DataFrame to list, then to sets
sym1 = set( symbol for symbol in df1[0].values.tolist() )
sym2 = set( symbol for symbol in df2[0].values.tolist() )
sym3 = set( symbol for symbol in df3[0].values.tolist() )
sym4 = set( symbol for symbol in df4[0].values.tolist() )

# join the 4 sets into one. Because it's a set, there will be no duplicate symbols
symbols = set.union( sym1, sym2, sym3, sym4 )

# Some stocks are 5 characters. Those stocks with the suffixes listed below are not of interest.
my_list = ['W', 'R', 'P', 'Q']
del_set = set()
sav_set = set()

for symbol in symbols:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set.add( symbol )
    else:
        sav_set.add( symbol )

print( f'Removed {len( del_set )} unqualified stock symbols...' )
print( f'There are {len( sav_set )} qualified stock symbols...' )



# Use your set of symbols
symbols = sav_set  # replace with your set of valid symbols

# Initialize a list to store the information
info_list = []

for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        info_list.append(info)
    except Exception as e:
        print(f"Could not retrieve data for {symbol}: {e}")

# Convert the list to a DataFrame
df = pd.DataFrame(info_list)

# At the time of fetching data, store the current time
data_fetch_time = datetime.now()

# You can add this timestamp as a new column to your DataFrame if needed
df['dataFetchTimestamp'] = data_fetch_time
