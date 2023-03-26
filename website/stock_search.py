import yfinance as yf


def get_stock_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.info

    if stock_info:
        stock_data = {
            "symbol": stock_info["symbol"],
            "company_name": stock_info["longName"],
            "current_price": stock_info["regularMarketPrice"],
        }
        return stock_data
    else:
        return None
