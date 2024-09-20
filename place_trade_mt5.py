import MetaTrader5 as mt5
import time
from datetime import datetime

# api_id = 23104224
# api_hash = 'b44355161c6b2938907b917c1c95905e'

api_id = 11014950
api_hash = 'eb0b24cf0210a85e2132470feb0106fa'

# Function to calculate the volume based on risk management (1% of account balance)
def calculate_volume(symbol, entry_price, stop_loss, account_balance, risk_percentage=1.0):
    pip_value = 0.1  # 1 pip is typically 0.1 for XAUUSD (check with your broker)
    stop_loss_distance = abs(entry_price - stop_loss) / pip_value
    max_loss = account_balance * (risk_percentage / 100)
    pip_value_per_lot = 10  # Standard pip value for 1 lot of XAUUSD (may vary by broker)
    required_volume = max_loss / (stop_loss_distance * pip_value_per_lot)
    volume = max(0.01, required_volume)  # Ensure the minimum volume is 0.01
    return volume

# Function to place trades on MetaTrader 5
def place_trade(symbol, trade_type, entry_price, stop_loss, tps, account_balance, current_price=None):

    # Limit orders: ORDER_TYPE_BUY_LIMIT, ORDER_TYPE_SELL_LIMIT
    # Market orders: ORDER_TYPE_BUY, ORDER_TYPE_SELL
    # Doc: https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_property_integer

    # market price
    if abs(current_price - entry_price) < 1:
        order_type = mt5.ORDER_TYPE_BUY if trade_type == 'BUY' else mt5.ORDER_TYPE_SELL

    # limit price
    else:
        order_type = mt5.ORDER_TYPE_BUY_LIMIT if trade_type == 'BUY' else mt5.ORDER_TYPE_SELL_LIMIT

    # volume = calculate_volume(symbol, entry_price, stop_loss, account_balance)
    volume = 0.3
    for i, tp in enumerate(tps, start=1):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": entry_price,
            "sl": stop_loss,
            "tp": tp,
            "deviation": 20,
            "magic": 234000,  # Unique identifier for this trade group
            "comment": f"Automated trade TP{i}",
            "type_time": mt5.ORDER_TIME_GTC,  # Good till canceled
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)

        # Print trade details
        print(f"Placing Trade #{i}")
        print(f"Symbol: {symbol}")
        print(f"Type: {trade_type}")
        print(f"Entry Price: {entry_price}")
        print(f"Stop Loss: {stop_loss}")
        print(f"Take Profit {i}: {tp}")
        print(f"Calculated Volume: {volume}")
        print(f"Trade Result: {result}\n")
        time.sleep(1)

def test_login():

    # connect to MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    print("Initialized successfully")

    # now connect to another trading account specifying the password
    account = 33012302
    authorized = mt5.login(account, password="!yJ0ZhOk", server="ACCapital-Demo") # ,
    if authorized:
        # display trading account data 'as is'
        print(mt5.account_info())
        # display trading account data in the form of a list
        print("Show account_info()._asdict():")
        account_info_dict = mt5.account_info()._asdict()
        for prop in account_info_dict:
            print("  {}={}".format(prop, account_info_dict[prop]))
    else:
        print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()

def login_mt5_demo():
    # connect to MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    print("Initialized successfully")

    # now connect to another trading account specifying the password
    account = 33012302
    authorized = mt5.login(account, password="!yJ0ZhOk", server="ACCapital-Demo")  # ,
    if authorized:
        # display trading account data 'as is'
        print(mt5.account_info())
        # display trading account data in the form of a list
        print("Show account_info()._asdict():")
        account_info_dict = mt5.account_info()._asdict()
        for prop in account_info_dict:
            print("  {}={}".format(prop, account_info_dict[prop]))

        return account_info_dict
    else:
        # print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
        raise Exception("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

# test_login()