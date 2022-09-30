from . import config
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

def get_btc_price():
    btc = client.get_symbol_ticker(symbol="BTCUSDT")
    btc_price = btc['price']
    btc_price_float = float(btc_price)

    return btc_price_float

print(get_btc_price())

def get_eth_price():
    eth = client.get_symbol_ticker(symbol="ETHUSDT")
    eth_price = eth['price']
    eth_price_float = float(eth_price)

    return eth_price_float

print(get_eth_price())

#candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)

#csvfile = open('1minuteBTC.csv', 'w', newline='')
#candlestick_writer = csv.writer(csvfile, delimiter=',')

#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE)


#for candlestick in  candlesticks:
 #   candlestick[0] = candlestick[0] / 1000
  #  candlestick_writer.writerow(candlestick)
  #csvfile.close()