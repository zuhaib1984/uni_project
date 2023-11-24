import yfinance as yf
from datetime import date
import time

# df = yf.download("AAPL",
#                  start="2023-01-01",
#                  interval='1h',
#                  end="2023-12-31")

def get_data(code):
     t = time.time()


while True:
    obj = yf.Ticker('AAPL')
    time.sleep(.5)
