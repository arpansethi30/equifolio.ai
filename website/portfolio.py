import pandas as pd
import yfinance as yf
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


nifty50_tickers = [
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "APOLLOHOSP.NS",
    "ASIANPAINT.NS",
    "AXISBANK.NS",
    "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS",
    "BAJAJFINSV.NS",
    "BPCL.NS",
    "BHARTIARTL.NS",
    "BRITANNIA.NS",
    "CIPLA.NS",
    "COALINDIA.NS",
    "DIVISLAB.NS",
    "DRREDDY.NS",
    "EICHERMOT.NS",
    "GRASIM.NS",
    "HCLTECH.NS",
    "HDFCBANK.NS",
    "HDFCLIFE.NS",
    "HEROMOTOCO.NS",
    "HINDALCO.NS",
    "HINDUNILVR.NS",
    "HDFC.NS",
    "ICICIBANK.NS",
    "ITC.NS",
    "INDUSINDBK.NS",
    "INFY.NS",
    "JSWSTEEL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "M&M.NS",
    "MARUTI.NS",
    "NTPC.NS",
    "NESTLEIND.NS",
    "ONGC.NS",
    "POWERGRID.NS",
    "RELIANCE.NS",
    "SBILIFE.NS",
    "SBIN.NS",
    "SUNPHARMA.NS",
    "TCS.NS",
    "TATACONSUM.NS",
    "TATAMOTORS.NS",
    "TATASTEEL.NS",
    "TECHM.NS",
    "TITAN.NS",
    "UPL.NS",
    "ULTRACEMCO.NS",
    "WIPRO.NS",
]

niftymidcap = [
    "ABB.NS",
    "AUBANK.NS",
    "ABBOTINDIA.NS",
    "ALKEM.NS",
    "ASHOKLEY.NS",
    "ASTRAL.NS",
    "AUROPHARMA.NS",
    "BALKRISIND.NS",
    "BATAINDIA.NS",
    "BHARATFORG.NS",
    "CANBK.NS",
    "COFORGE.NS",
    "CONCOR.NS",
    "CUMMINSIND.NS",
    "ESCORTS.NS",
    "FEDERALBNK.NS",
    "GODREJPROP.NS",
    "GUJGASLTD.NS",
    "HINDPETRO.NS",
    "HONAUT.NS",
    "IDFCFIRSTB.NS",
    "INDHOTEL.NS",
    "JINDALSTEL.NS",
    "JUBLFOOD.NS",
    "LTTS.NS",
    "LICHSGFIN.NS",
    "LUPIN.NS",
    "MRF.NS",
    "M&MFIN.NS",
    "MFSL.NS",
    "OBEROIRLTY.NS",
    "OFSS.NS",
    "PAGEIND.NS",
    "PERSISTENT.NS",
    "PETRONET.NS",
    "POLYCAB.NS",
    "PFC.NS",
    "PNB.NS",
    "RECLTD.NS",
    "SRTRANSFIN.NS",
    "SAIL.NS",
    "TVSMOTOR.NS",
    "TATACOMM.NS",
    "TORNTPOWER.NS",
    "TRENT.NS",
    "UBL.NS",
    "IDEA.NS",
    "VOLTAS.NS",
    "ZEEL.NS",
    "ZYDUSLIFE.NS",
]


def get_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock_data = yf.download(ticker, start="2013-01-01", end="2023-03-21")
        data[ticker] = stock_data["Adj Close"]
    return pd.DataFrame(data)


def optimize_portfolio(data, investment_amount):
    mu = expected_returns.mean_historical_return(data)
    S = risk_models.sample_cov(data)

    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()

    latest_prices = get_latest_prices(data)
    da = DiscreteAllocation(
        cleaned_weights, latest_prices, total_portfolio_value=investment_amount
    )
    allocation, leftover = da.greedy_portfolio()

    return allocation, leftover
