import time
import datetime as dt
import yfinance as yf

# Parameters
short_window = 20
long_window = 50

initial_balance = 10000  # USD
balance = initial_balance
position = 0  # EUR
forex_pair = 'EURUSD=X'

# Download the latest 1-day data at 1-minute intervals
data = yf.download(forex_pair, period='5d', interval='2m', progress=False)

# Calculate Short and Long SMAs
data['SMA_Short'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['SMA_Long'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

# Iterate over rows for trading logic
for index, row in data.iterrows():
    # Buy if short SMA > long SMA and not in position
    if row['SMA_Short'] > row['SMA_Long'] and position == 0:
        units_to_buy = balance // row['Close']
        balance -= units_to_buy * row['Close']
        position += units_to_buy

        print(f'{dt.datetime.now()}: Bought {units_to_buy} EUR for {row["Close"]:.2f} USD per unit')

    # Sell if short SMA < long SMA and holding a position
    elif row['SMA_Short'] < row['SMA_Long'] and position > 0:
        balance += position * row['Close']
        print(f'{dt.datetime.now()}: Sold {position} EUR for {row["Close"]:.2f} USD per unit')
        position = 0

    # If holding, do nothing
    else:
        print(f'{dt.datetime.now()}: Holding {position} EUR at {row["Close"]:.2f} USD per unit')


# Calculate the final balance
final_balance = balance + position * data.iloc[-1]['Close']
print(f'Final Balance: ${final_balance:.2f}')

# Output performance
if final_balance > initial_balance:
    print(f'Balance was increased by {(final_balance / initial_balance - 1) * 100:.2f}%')
elif final_balance < initial_balance:
    print(f'Balance was decreased by {(1 - final_balance / initial_balance) * 100:.2f}%')
else:
    print('Balance did not change')
