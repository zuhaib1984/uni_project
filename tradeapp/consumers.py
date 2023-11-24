import time
import json
import pandas as pd
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import yfinance as yf
import asyncio
import talib as ta


def sma(df, window=20):
    return df.rolling(window=window).mean()


def rstd(df, window=20):
    return df.rolling(window=window).std()


def get_tp(df):
    return (df["High"] + df["Low"] + df["Close"]) / 3


def bollinger_band(df, window=20):
    df["TP"] = get_tp(df)
    df["SMA"] = df["TP"].rolling(window=window).mean()
    df["STD"] = df["TP"].rolling(window=window).std()
    df["UB"] = df["SMA"] + 2 * df["STD"]
    df["LB"] = df["SMA"] - 2 * df["STD"]

    return df


def relative_strength_index(df, timeperiod=14):
    df["RSI"] = ta.RSI(df["Close"], timeperiod=timeperiod)
    return df


def simple_moving_average(df, acceleration=0.02, maximum=0.2):
    df["SMA"] = ta.SAR(
        df["High"], df["Close"], acceleration=acceleration, maximum=maximum
    )
    return df


def is_volatileBB(df):
    tail = df.tail(5)
    return [abs(tail["RTH"][-1]) > 4, tail["RTH"][-1] > 0]  # Zero is placeholder


def get_signal(df):
    df["vol"] = df["UB"] - df["LB"]

    df["RTH"] = df["vol"].pct_change(1) * 100
    volatile, side = is_volatileBB(df)
    if not side and volatile:
        signal = "Sell Assets"
    elif volatile and side:
        signal = "Buy Asset"
    else:
        signal = "Hold"
    return signal


class GetSignalConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        params = json.loads(text_data)
        timeperiod = int(params["timeperiod"])
        maximum = float(params["maximum"])
        acceleration = float(params["acceleration"])
        while True:
            df = yf.download(tickers=params["asset"], period="1d", interval="1m").tail(
                100
            )
            df = bollinger_band(df, window=timeperiod)
            df = relative_strength_index(
                df,
            )
            df = simple_moving_average(df, acceleration=acceleration, maximum=maximum)
            df_json = df.tail(80).to_json()
            signal = get_signal(df)

            await self.send(json.dumps({"data": df_json, "signal": signal}))
            await asyncio.sleep(5)
