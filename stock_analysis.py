import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid', palette='Set2', font_scale=1.1)
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'

# 1. Get data (3 Indian stocks, last 2 years)
stocks = ['TCS.NS', 'INFY.NS', 'RELIANCE.NS']
frames = []
for s in stocks:
    d = yf.Ticker(s).history(period='2y')
    d['stock'] = s
    frames.append(d)

df = pd.concat(frames).reset_index()
df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
df = df[['Date', 'stock', 'Close', 'Volume']].dropna()
print("Shape:", df.shape)
df.to_csv('stock_clean.csv', index=False)

# 2. Price trend
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='Close', hue='stock', linewidth=2)
plt.title('Stock Price Trend')
plt.xlabel('Date')
plt.ylabel('Close Price (INR)')
plt.savefig('stock_price.png', dpi=300, bbox_inches='tight')
plt.show()

# 3. Moving averages (TCS)
tcs = df[df['stock'] == 'TCS.NS'].copy()
tcs['MA50'] = tcs['Close'].rolling(50).mean()
tcs['MA200'] = tcs['Close'].rolling(200).mean()

plt.figure(figsize=(12, 6))
plt.plot(tcs['Date'], tcs['Close'], label='Close')
plt.plot(tcs['Date'], tcs['MA50'], label='50-day MA')
plt.plot(tcs['Date'], tcs['MA200'], label='200-day MA')
plt.title('TCS: Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (INR)')
plt.legend()
plt.savefig('stock_moving_avg.png', dpi=300, bbox_inches='tight')
plt.show()

# 4. Volatility (30-day rolling std of daily returns)
df['return'] = df.groupby('stock')['Close'].pct_change()
df['volatility'] = df.groupby('stock')['return'].transform(
    lambda x: x.rolling(30).std())

plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='volatility', hue='stock', linewidth=2)
plt.title('Stock Volatility (30-day)')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.savefig('stock_volatility.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nStock Market Analysis Completed!")