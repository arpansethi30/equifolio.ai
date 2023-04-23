from flask import Blueprint, render_template, request, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import ContactUs
from . import db
import json

import pandas as pd
import yfinance as yf
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

# from my_module import my_function
import sys
from pathlib import Path

# Add the current directory to the Python import paths
current_directory = Path(__file__).resolve().parent
sys.path.append(str(current_directory))
from portfolio import get_stock_data, optimize_portfolio

# Import your function
# from my_module import generate_portfolio

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", user=current_user)


@views.route("/graph", methods=["GET", "POST"])
@login_required
def graph():
    return render_template("graph.html", user=current_user)


@views.route("/equifolio.ai", methods=["GET", "POST"])
def home():
    return render_template("index.html", user=current_user)


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


@views.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    if request.method == "POST":
        investment_amount = float(request.form["investment_amount"])
        stock_data = get_stock_data(nifty50_tickers)
        allocation, leftover = optimize_portfolio(stock_data, investment_amount)
        return render_template(
            "result.html", allocation=allocation, leftover=leftover, user=current_user
        )
    return render_template("portfolio.html", user=current_user)


@views.route("/pricing", methods=["GET", "POST"])
def pricing():
    return render_template("pricing.html", user=current_user)


@views.route("/stock_analysis", methods=["GET", "POST"])
def stock_analysis():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        return render_template("stock_analysis.html", symbol=symbol, user=current_user)
    return render_template("stock_analysis_form.html", user=current_user)


@views.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html", user=current_user)


@views.route("/about", methods=["GET", "POST"])
def about():
    return render_template("AboutUs.html", user=current_user)


# @views.route("/search", methods=["GET"])
# def search_stocks():
#     search_query = request.args.get("q")
#     if search_query:
#         stock = yf.Ticker(f"{search_query}.NS")
#         if stock.info:
#             stock_info = {
#                 "symbol": stock.info["symbol"],
#                 "name": stock.info["longName"],
#                 "price": round(stock.info["regularMarketPrice"], 2),
#                 "change": round(stock.info["regularMarketChange"], 2),
#                 "percent_change": round(stock.info["regularMarketChangePercent"], 2),
#             }
#             return render_template("search.html", stock_info=stock_info)
#         else:
#             return render_template("search.html", error="Unable to fetch stock data.")
#     else:
#         return render_template("search.html", error="Missing search query.")


@views.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        symbol = request.form["symbol"]
        ticker = yf.Ticker(symbol)
        if ticker.info:
            return render_template("search_results.html", symbol=symbol)
        else:
            return render_template("search.html", error="Invalid symbol")
    else:
        return render_template("search.html")


@views.route("/search_results")
def search_results():
    symbol = request.args.get("symbol")
    ticker = yf.Ticker(symbol)
    info = ticker.info
    return render_template("search_results.html", symbol=symbol, info=info)
