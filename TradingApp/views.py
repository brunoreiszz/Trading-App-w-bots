from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .get_prices import get_btc_price, get_eth_price
from .models import Balance, Asset, User
from . import db
import json
from . import config
from binance.client import Client
from binance.enums import *


views = Blueprint('views', __name__)

client = Client(config.API_KEY, config.API_SECRET)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_balance = Balance.query.filter_by(id=current_user.id).first()
    user_assets = Asset.query.filter_by(id=current_user.id).first()
#    if request.method == 'POST':
#        note = request.form.get('note')
#
#        if len(note) < 1:
#            flash('Note is too short!', category='error')
#        else:
#            new_note = Balance(data=note, user_id=current_user.id)
#            db.session.add(new_note)
#            db.session.commit()
#            flash('Note added!', category='success')

    return render_template("home.html", user=current_user, balance=user_balance, asset=user_assets)


@views.route('/indicators', methods=['GET', 'POST'])
@login_required
def indicators():

    return render_template("indicators.html", user=current_user)


@views.route('/tradeeth', methods=['GET', 'POST'])
@login_required
def eth():
    user_balance = Balance.query.filter_by(id=current_user.id).first()
    user_assets = Asset.query.filter_by(id=current_user.id).first()

    return render_template("ETH.html", user=current_user, balance=user_balance, asset=user_assets)



@views.route('/tradebtc', methods=['GET', 'POST'])
@login_required
def btc():
    user_balance = Balance.query.filter_by(id=current_user.id).first()    
    user_assets = Asset.query.filter_by(id=current_user.id).first()

    return render_template("BTC.html", user=current_user, balance=user_balance, asset=user_assets)


@views.route('/historybtc')
def historybtc():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 week ago UTC")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)
    
    return jsonify(processed_candlesticks)


@views.route('/historyeth')
def historyeth():
    candlesticks = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 week ago UTC")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)
    
    return jsonify(processed_candlesticks)


@views.route('/buybtc', methods=["POST"])
@login_required
def buy_btc():  
    user_assets = Asset.query.filter_by(id=current_user.id).first()
    user_balance = Balance.query.filter_by(id=current_user.id).first()

    user_current_balance = user_balance.balance
    user_balance_float = float(user_current_balance)
    btc_buy_price = get_btc_price()

    user_current_asset = user_assets.btc_balance
    user_btc_int = int(user_current_asset)

    if user_balance_float < btc_buy_price:
        return "You don't have enough balance"
    else:
        user_new_btc = user_btc_int + 1
        user_assets.btc_balance = user_new_btc
        db.session.commit()

        user_new_balance = user_balance_float - btc_buy_price
        user_balance.balance = user_new_balance
        db.session.commit()

        return render_template('BTC.html', user=current_user, balance=user_balance, asset=user_assets)


@views.route('/sellbtc', methods=["POST"])
@login_required
def sell_btc():  
    user_assets = Asset.query.filter_by(id=current_user.id).first()
    user_balance = Balance.query.filter_by(id=current_user.id).first()

    user_current_balance = user_balance.balance
    user_balance_float = float(user_current_balance)
    btc_sell_price = get_btc_price()

    user_current_asset = user_assets.btc_balance
    user_btc_int = int(user_current_asset)

    if user_btc_int <= 0:
        return "You don't have BTC to sell"
    else:
        user_new_btc = user_btc_int - 1
        user_assets.btc_balance = user_new_btc
        db.session.commit()

        user_new_balance = user_balance_float + btc_sell_price
        user_balance.balance = user_new_balance
        db.session.commit()

    return render_template('BTC.html', user=current_user, balance=user_balance, asset=user_assets)


@views.route('/buyeth', methods=["POST"])
@login_required
def buy_eth():  
    user_assets = Asset.query.filter_by(id=current_user.id).first()
    user_balance = Balance.query.filter_by(id=current_user.id).first()

    user_current_balance = user_balance.balance
    user_balance_float = float(user_current_balance)
    eth_buy_price = get_eth_price()

    user_current_asset = user_assets.eth_balance
    user_eth_int = int(user_current_asset) 

    if user_balance_float < eth_buy_price:
        return "You don't have enough balance"
    else:
        user_new_eth = user_eth_int + 1
        user_assets.eth_balance = user_new_eth
        db.session.commit()

        user_new_balance = user_balance_float - eth_buy_price
        user_balance.balance = user_new_balance
        db.session.commit()

        return render_template('ETH.html', user=current_user, balance=user_balance, asset=user_assets)


@views.route('/selleth', methods=["POST"])
@login_required
def sell_eth():  
    user_assets = Asset.query.filter_by(id=current_user.id).first()
    user_balance = Balance.query.filter_by(id=current_user.id).first()

    user_current_balance = user_balance.balance
    user_balance_float = float(user_current_balance)
    eth_sell_price = get_eth_price()

    user_current_asset = user_assets.eth_balance
    user_eth_int = int(user_current_asset) 

    if user_eth_int <= 0:
        return "You don't have ETH to sell"
    else:
        user_new_eth = user_eth_int - 1
        user_assets.eth_balance = user_new_eth
        db.session.commit()
        
        user_new_balance = user_balance_float + eth_sell_price
        user_balance.balance = user_new_balance
        db.session.commit()

    return render_template('ETH.html', user=current_user, balance=user_balance, asset=user_assets)


#@views.route('/run_rsi_bot_eth', methods=["GET", "POST"])
#@login_required
#def rsi_bot_eth():
#    user_assets = Asset.query.filter_by(id=current_user.id).first()
#    user_balance = Balance.query.filter_by(id=current_user.id).first()
#
#    if request.method == "POST":
#        run_eth_stochrsi_bot()


#        in_position, num_trades, price_buy, price_sell, pnl = run_eth_stochrsi_bot()
        #in_position = get_results[0]
        #num_trades = get_results[1]
        #price_buy = get_results[2]
        #price_sell = get_results[3]
        #pnl = get_results[4]           RETURN LIST, THEN GET VALUES INDIVIDUALLY?

#        if in_position == True:

#            user_current_balance = user_balance.balance
#            user_balance_float = float(user_current_balance)
#            user_new_balance = user_balance_float - price_buy
#            user_balance.balance = user_new_balance
#            db.session.commit()

#            return render_template("ETH.html", user=current_user, balance=user_balance, asset=user_assets)



#@views.route('/delete-note', methods=['POST'])
#def delete_note():
#    note = json.loads(request.data)
#    noteId = note['noteId']
#    note = Note.query.get(noteId)
#    if note:
#        if note.user_id == current_user.id:
#            db.session.delete(note)
#            db.session.commit()

#    return jsonify({})

