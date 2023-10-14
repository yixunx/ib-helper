#%%
from ib_insync import *
import nest_asyncio

nest_asyncio.apply()


def butterfly(middle_strike, wing, expiration, symbol='SPY', opt_type='CALL'):
    # Define the underlying stock
    exchange = 'SMART'
    currency = 'USD'

    # Define the three strike prices
    lower_strike = middle_strike - wing
    higher_strike = middle_strike + wing

    # Create the option legs
    lower_leg = Option(symbol, expiration, lower_strike, opt_type, exchange)
    middle_leg = Option(symbol, expiration, middle_strike, opt_type, exchange)
    higher_leg = Option(symbol, expiration, higher_strike, opt_type, exchange)
    ib.qualifyContracts(lower_leg, middle_leg, higher_leg)

    legs = [
        ComboLeg(conId=lower_leg.conId, action='BUY', ratio=1),
        ComboLeg(conId=middle_leg.conId, action='SELL', ratio=2),
        ComboLeg(conId=higher_leg.conId, action='BUY', ratio=1)
    ]

    return Bag(symbol=symbol, exchange=exchange, comboLegs=legs, currency = currency)

def market_buy(contract, quantity=1):
    ib.placeOrder(contract, MarketOrder('BUY', quantity))

def market_sell(contract, quantity=1):
    ib.placeOrder(contract, MarketOrder('SELL', quantity))

#%%
# Connect to IB
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)

# Set the expiry to your desired expiry date for the option
expiry = "20231018" # For example, set it to "YYYYMMDD" format

#%%
# Submit the bracket order with a specific strike price

#%%
# Disconnect from IB
ib.disconnect()
