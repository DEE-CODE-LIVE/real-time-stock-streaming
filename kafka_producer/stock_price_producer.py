import requests
import time
import json
from kafka import KafkaProducer

API_KEY = 'd27445pr01qloarhdtmgd27445pr01qloarhdtn0'
TICKER = 'AAPL'  # or any stock symbol like 'TSLA', 'MSFT'

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_stock_price():
    url = f'https://finnhub.io/api/v1/quote?symbol={TICKER}&token={API_KEY}'
    response = requests.get(url)
    data = response.json()
    data['symbol'] = TICKER
    data['timestamp'] = int(time.time())
    return data

while True:
    stock_data = get_stock_price()
    producer.send('stock_prices', stock_data)
    print(f"Sent: {stock_data}")
    time.sleep(1)
