from flask import Blueprint, render_template, request, url_for, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import ContactUs, User, WatchlistItem
from . import db
import json
import pandas as pd
import yfinance as yf
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from datetime import timedelta

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
    if current_user.is_authenticated:
        return redirect(url_for("views.dashboard"))
    return render_template("index.html", user=current_user)


@views.route("/logged", methods=["GET"])
@login_required
def dashboard():
    return render_template("watchlist.html", user=current_user)


@views.route("/graph", methods=["GET", "POST"])
@login_required
def graph():
    return render_template("graph.html", user=current_user)


@views.route("/", methods=["GET", "POST"])
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
    # "SRTRANSFIN.NS",
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


@views.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    if request.method == "POST":
        investment_amount = float(request.form["investment_amount"])
        risk_preference = request.form["risk_preference"]
        stock_data = get_stock_data(nifty50_tickers, niftymidcap, risk_preference)
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


@views.route("/add_stock_to_watchlist", methods=["POST"])
@login_required
def add_stock_to_watchlist():
    stock_symbol = request.form.get("stock_symbol")
    if not stock_symbol:
        flash("Stock symbol cannot be empty.", category="error")
    else:
        new_watchlist_item = WatchlistItem(
            stock_symbol=stock_symbol, user_id=current_user.id
        )
        db.session.add(new_watchlist_item)
        db.session.commit()
        flash("Stock added to watchlist!", category="success")
    return redirect(url_for("views.view_watchlist"))


def get_stock_price_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    history = stock.history(period="6mo")
    return history


def calculate_percentage_change(current_price, past_price):
    change = ((current_price - past_price) / past_price) * 100
    return round(change, 2)


@views.route("/view_watchlist")
@login_required
def view_watchlist():
    user_watchlist = WatchlistItem.query.filter_by(user_id=current_user.id).all()
    stock_data = []

    for watchlist_item in user_watchlist:
        stock_history = get_stock_price_data(watchlist_item.stock_symbol)
        latest_price = stock_history.iloc[-1]["Close"]
        day_change = calculate_percentage_change(
            latest_price, stock_history.iloc[-2]["Close"]
        )
        week_change = calculate_percentage_change(
            latest_price, stock_history.iloc[-6]["Close"]
        )
        month_change = calculate_percentage_change(
            latest_price, stock_history.iloc[-21]["Close"]
        )
        six_month_change = calculate_percentage_change(
            latest_price, stock_history.iloc[0]["Close"]
        )

        stock_data.append(
            {
                "id": watchlist_item.id,
                "symbol": watchlist_item.stock_symbol,
                "latest_price": latest_price,
                "day_change": day_change,
                "week_change": week_change,
                "month_change": month_change,
                "six_month_change": six_month_change,
            }
        )

    return render_template("watchlist.html", user=current_user, stock_data=stock_data)


@views.route("/remove_stock_from_watchlist/<int:watchlist_item_id>")
@login_required
def remove_stock_from_watchlist(watchlist_item_id):
    watchlist_item = WatchlistItem.query.get(watchlist_item_id)
    if watchlist_item:
        if watchlist_item.user_id == current_user.id:
            db.session.delete(watchlist_item)
            db.session.commit()
            flash("Stock removed from watchlist.", category="success")
        else:
            flash(
                "You do not have permission to remove this stock from the watchlist.",
                category="error",
            )
    else:
        flash("Stock not found in watchlist.", category="error")
    return redirect(url_for("views.view_watchlist"))
