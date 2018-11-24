# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
# DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
# WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy
import pandas
from scipy import stats
from statsmodels import robust
import math
import requests
import json
import time
import random
from time import localtime, strftime
import datetime
import calendar
from random import shuffle
import pytz
#####################################
# Error Handling
import traceback
import sys
# Time stuff
set(pytz.all_timezones_set)
tz = pytz.timezone('Europe/London')
# https://gist.github.com/mjrulesamrat/0c1f7de951d3c508fb3a20b4b0b33a98
YEAR_var = 2018
market_close_tm = "07:59"
market_open_tm = "16:59"

#CREDS###################################################################
LIVE_API_KEY = ''
LIVE_USERNAME = ""
LIVE_PASSWORD = ""
LIVE_ACC_ID = ""
##########################################################################
DEMO_API_KEY = ''
DEMO_USERNAME = ""
DEMO_PASSWORD = ""
DEMO_ACC_ID = ""
###########################################################################

b_REAL = True
b_Contrarian = False  # DO NOT SET

if b_REAL:
    REAL_OR_NO_REAL = 'https://api.ig.com/gateway/deal'
    API_ENDPOINT = "https://api.ig.com/gateway/deal/session"
    API_KEY = LIVE_API_KEY
    data = {"identifier": LIVE_USERNAME, "password": LIVE_PASSWORD}
else:
    REAL_OR_NO_REAL = 'https://demo-api.ig.com/gateway/deal'
    API_ENDPOINT = "https://demo-api.ig.com/gateway/deal/session"
    API_KEY = DEMO_API_KEY
    data = {"identifier": DEMO_USERNAME, "password": DEMO_PASSWORD}

headers = {'Content-Type': 'application/json; charset=utf-8',
           'Accept': 'application/json; charset=utf-8',
           'X-IG-API-KEY': API_KEY,
           'Version': '2'
           }

r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

headers_json = dict(r.headers)
CST_token = headers_json["CST"]
print(R"CST : " + CST_token)
x_sec_token = headers_json["X-SECURITY-TOKEN"]
print(R"X-SECURITY-TOKEN : " + x_sec_token)

# GET ACCOUNTS
base_url = REAL_OR_NO_REAL + '/accounts'
authenticated_headers = {'Content-Type': 'application/json; charset=utf-8',
                         'Accept': 'application/json; charset=utf-8',
                         'X-IG-API-KEY': API_KEY,
                         'CST': CST_token,
                         'X-SECURITY-TOKEN': x_sec_token}

auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

base_url = REAL_OR_NO_REAL + '/session'

if b_REAL:
    data = {
        "accountId": LIVE_ACC_ID,
        "defaultAccount": "True"}  # Main Live acc
else:
    data = {
        "accountId": DEMO_ACC_ID,
        "defaultAccount": "True"}  # Main Demo acc

auth_r = requests.put(
    base_url,
    data=json.dumps(data),
    headers=authenticated_headers)

# print("-----------------DEBUG-----------------")
# print("#################DEBUG#################")
# print(auth_r.status_code)
# print(auth_r.reason)
# print(auth_r.text)
# print("-----------------DEBUG-----------------")
# print("#################DEBUG#################")


##########################################################################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################################################################

###########################################################################
###########################################################################
###########################################################################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
###########################################################################
###########################################################################
###########################################################################
# PROGRAMMABLE VALUES, IG specific.
# SET INITIAL VARIABLES
orderType_value = "MARKET"
size_value = "10"
expiry_value = "DFB"
guaranteedStop_value = True
currencyCode_value = "GBP"
forceOpen_value = True
###########################################################################
profit_indicator_multiplier = 5
ESMA_new_margin = 21                    # (20% for stocks)
too_high_margin = 100                   # No stupidly high pip limit per trade
# Normally would be 3/22 days but dull stocks require a lower multiplier
ce_multiplier = 2
max_trades = int(int(size_value) * 1)   # Max Trades (total per point) Per Epic
spread_check = -3                       # Low spread
acc_used_pct = 85                       # How much of account to use
greed_indicator = 99999                 # Dont hang onto profitable trades too long
SUPER_LOW_NEG_MARGIN = 100          # Dont trust IG to take care of ESMA margins

# You will need to change this bit depending on if you are using Live/Demo as the NodeID's are different.
# From IG:
	# "the live environment subscribes to different Id numbers. To manually
	# navigate your way to the correct share is to go to the "Browse Markets"
	# and leave the input field blank and click on go market, you will see a
	# list of all markets offered then you can click on Shares UK:
	# https://i.imgur.com/qsZFpZ0.png"

# I hope this helps.

types = {
    # 'Cryptocurrency': '',
    # 'Options (Australia 200)': '',
    # 'Weekend Indices': '',
    # 'Indices': '',
    # 'Forex': '',
    # 'Commodities Metals Energies': '',
    # 'Bonds and Moneymarket': '',
    # 'ETFs, ETCs & Trackers': '',
    'Shares - UK': ['', 'Europe/London'],
    'Shares - UK International (IOB)': ['', 'Europe/London'],
    # 'Shares - US (All Sessions)': '',
    # 'Shares - US': '',
    # 'Shares - Austria': '',
    # 'Shares - Belgium': '',
    'Shares - LSE (UK)': ['', 'Europe/London']}
# 'Shares - Finland': '',
# 'Shares - Canada': '',
# 'Shares - France': '',
# 'Shares - Denmark': '',
# 'Shares - Germany': '',
# 'Shares - Greece': '',
# 'Shares - Hong Kong': '',
# 'Shares - Ireland (ISEQ)': '',
# 'Shares - Ireland (LSE)': '',
# 'Shares - Netherlands': '',
# 'Shares - Norway': '',
# 'Shares - Portugal': '',
# 'Shares - Singapore': '',
# 'Shares - South Africa': '',
# 'Shares - Sweden': '',
# 'Shares - Switzerland': '',
# 'Options (Eu Stocks 50)': '',
# 'Options (France 40)': '',
# 'Options (FTSE)': '',
# 'Options (Germany)': '',
# 'Options (Italy 40)': '',
# 'Options (Spain 35)': '',
# 'Options (Sweden 30)': '',
# 'Options (US 500)': '',
# 'Options (Wall St)': '',
# 'Options on FX Majors': '',
# 'Options on Metals, Energies': ''}

###########################################################################
###########################################################################
###########################################################################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
###########################################################################
###########################################################################
###########################################################################


def debug_info(err_str):
    # Standard debugging function, pass it a string
    print("-----------------DEBUG-----------------")
    print("#################DEBUG#################")
    print(str(time.strftime("%H:%M:%S")) + ":!!!DEBUG!!!:" + str(err_str))
    print("#################DEBUG#################")
    print("-----------------DEBUG-----------------")


def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]


def percentage(part, whole):
    return 100 * float(part) / float(whole)


def percentage_of(percent, whole):
    # percent should always be 20 for stocks
    # ESMA regulations calculating min stop loss (20% for stocks)
    return (percent * whole) / 100.0


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)


def idTooMuchPositions(key, positionMap):
    if((key in positionMap) and (int(positionMap[key]) >= int(max_trades))):
        return True
    else:
        return False


def try_market_order(epic_id, trade_direction, limit, stop_pips, positionMap):

    if trade_direction == "NONE":
        return None

    key = epic_id + '-' + trade_direction
    # print(str(key) + " has position of " + str(positionMap[key]))
    if idTooMuchPositions(key, positionMap):
        print(str(key) +
              " has position of " +
              str(positionMap[key]) +
              ", hence should not trade")
        return None

    no_trade_window()  # last chance to bail to avoid neg balance

    limitDistance_value = str(limit)  # Limit
    stopDistance_value = str(stop_pips)  # Stop

    ##########################################################################
    print(
        "Order will be a " +
        str(trade_direction) +
        " Order, With a limit of: " +
        str(limitDistance_value))
    print(
        "stopDistance_value for " +
        str(epic_id) +
        " will bet set at " +
        str(stopDistance_value))
    ##########################################################################

    # MAKE AN ORDER
    base_url = REAL_OR_NO_REAL + '/positions/otc'
    data = {
        "direction": trade_direction,
        "epic": epic_id,
        "limitDistance": limitDistance_value,
        "orderType": orderType_value,
        "size": size_value,
        "expiry": expiry_value,
        "guaranteedStop": guaranteedStop_value,
        "currencyCode": currencyCode_value,
        "forceOpen": forceOpen_value,
        "stopDistance": stopDistance_value}
    r = requests.post(
        base_url,
        data=json.dumps(data),
        headers=authenticated_headers)

    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")
    # print(r.status_code)
    # print(r.reason)
    # print(r.text)
    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")

    d = json.loads(r.text)
    deal_ref = d['dealReference']
    time.sleep(1)
    # CONFIRM MARKET ORDER
    base_url = REAL_OR_NO_REAL + '/confirms/' + deal_ref
    auth_r = requests.get(base_url, headers=authenticated_headers)
    d = json.loads(auth_r.text)
    DEAL_ID = d['dealId']
    print("DEAL ID : " + str(d['dealId']))
    print(d['dealStatus'])
    print(d['reason'])

    if str(d['reason']) != "SUCCESS":
        print("some thing occurred ERROR!!")
        time.sleep(5)
        print("!!!INFO!!!...Order failed, Check IG Status, Resuming...")
    else:
        print("!!INFO!!...Yay, ORDER OPEN")
        time.sleep(3)


def Chandelier_Exit_formula(TRADE_DIR, ATR, Price):
    # Chandelier Exit (long) = 22-day High - ATR(22) x 3
    # Chandelier Exit (short) = 22-day Low + ATR(22) x 3

    if TRADE_DIR == "BUY":

        return float(Price) - float(ATR) * int(ce_multiplier)

    elif TRADE_DIR == "SELL":

        return float(Price) + float(ATR) * int(ce_multiplier)


def calculate_stop_loss(d):

    price_ranges = []
    closing_prices = []
    first_time_round_loop = True
    TR_prices = []
    price_compare = "bid"

    for i in d['prices']:
        if first_time_round_loop:
            ###########################################
            # First time round loop cannot get previous
            ###########################################
            closePrice = i['closePrice'][price_compare]
            closing_prices.append(closePrice)
            high_price = i['highPrice'][price_compare]
            low_price = i['lowPrice'][price_compare]
            price_range = float(high_price - closePrice)
            price_ranges.append(price_range)
            first_time_round_loop = False
        else:
            prev_close = closing_prices[-1]
            ###########################################
            closePrice = i['closePrice'][price_compare]
            closing_prices.append(closePrice)
            high_price = i['highPrice'][price_compare]
            low_price = i['lowPrice'][price_compare]
            price_range = float(high_price - closePrice)
            price_ranges.append(price_range)
            TR = max(high_price - low_price,
                     abs(high_price - prev_close),
                     abs(low_price - prev_close))
            TR_prices.append(TR)

    return str(int(float(max(TR_prices))))


def main_trade_function(epic_id):

    position_base_url = REAL_OR_NO_REAL + "/positions"
    position_auth_r = requests.get(
        position_base_url, headers=authenticated_headers)
    position_json = json.loads(position_auth_r.text)

    positionMap = {}

    # print("-------------Position Info-------------")
    # print("#################DEBUG#################")
    # print(position_auth_r.status_code)
    # print(position_auth_r.reason)
    # print(position_auth_r.text)
    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")

    for item in position_json['positions']:
        direction = item['position']['direction']
        dealSize = item['position']['dealSize']
        ccypair = item['market']['epic']
        key = ccypair + '-' + direction
        if(key in positionMap):
            positionMap[key] = dealSize + positionMap[key]
        else:
            positionMap[key] = dealSize
    print('current position summary:')
    print(positionMap)

    try:

        # obligatory sleep, gets round IG 60 per min limit
        time.sleep(2)

        base_url = REAL_OR_NO_REAL + "/prices/" + epic_id + "/WEEK/18"
        # Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5,
        # MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3,
        # HOUR_4, DAY, WEEK, MONTH)
        auth_r = requests.get(base_url, headers=authenticated_headers)
        d = json.loads(auth_r.text)

        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")
        # print(auth_r.status_code)
        # print(auth_r.reason)
        # print(auth_r.text)
        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")

        remaining_allowance = d['allowance']['remainingAllowance']
        reset_time = humanize_time(
            int(d['allowance']['allowanceExpiry']))
        print("-----------------INFO-----------------")
        print("#################INFO#################")
        print("Remaining API Calls left: " + str(remaining_allowance))
        print("Time to API Key reset: " + str(reset_time))
        print("-----------------INFO-----------------")
        print("#################INFO#################")

        ATR = calculate_stop_loss(d)
        high_prices = []
        low_prices = []

        for i in d['prices']:

            if i['highPrice']['bid'] is not None:
                highPrice = i['highPrice']['bid']
                high_prices.append(highPrice)
            ########################################
            if i['lowPrice']['bid'] is not None:
                lowPrice = i['lowPrice']['bid']
                low_prices.append(lowPrice)

        low_prices = numpy.ma.asarray(low_prices)
        high_prices = numpy.ma.asarray(high_prices)

        xi = numpy.arange(0, len(low_prices))

        low_prices_slope, low_prices_intercept, low_prices_lo_slope, low_prices_hi_slope = stats.mstats.theilslopes(
            low_prices, xi, 0.99)
        high_prices_slope, high_prices_intercept, high_prices_lo_slope, high_prices_hi_slope = stats.mstats.theilslopes(
            high_prices, xi, 0.99)

        base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
        auth_r = requests.get(
            base_url, headers=authenticated_headers)
        d = json.loads(auth_r.text)

        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")
        # print(auth_r.status_code)
        # print(auth_r.reason)
        # print(auth_r.text)
        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")

        current_bid = d['snapshot']['bid']

        # # HIGH (IQR)
        # var_upper = float(high_prices_intercept +
        # (abs(stats.iqr(high_prices, nan_policy='omit') * 2)))
        # # LOW (IQR)
        # var_lower = float(low_prices_intercept -
        # (abs(stats.iqr(low_prices, nan_policy='omit') * 2)))

        # HIGH (MAD)
        var_upper = float(
            high_prices_intercept + (abs(robust.mad(high_prices) * 3)))
        # LOW (MAD)
        var_lower = float(low_prices_intercept -
                          (abs(robust.mad(low_prices) * 3)))

        if float(current_bid) > float(var_upper):
            trade_direction = "BUY"
        elif float(current_bid) < float(var_lower):
            trade_direction = "SELL"
        else:
            pip_limit = 9999999  # Junk Data
            stop_pips = "999999"  # Junk Data
            trade_direction = "NONE"
            debug_info("Nope")

        if trade_direction == "BUY":
            pip_limit = int(abs(float(max(high_prices)) -
                                float(current_bid)) * profit_indicator_multiplier)
            ce_stop = Chandelier_Exit_formula(
                trade_direction, ATR, min(low_prices))
            stop_pips = str(int(abs(float(current_bid) - (ce_stop))))
            print("!!INFO!!...BUY!!")
            print(str(epic_id))
            print(
                "!!INFO!!...Take Profit@...." +
                str(pip_limit) +
                " pips")
        elif trade_direction == "SELL":
            pip_limit = int(abs(float(min(low_prices)) -
                                float(current_bid)) * profit_indicator_multiplier)
            ce_stop = Chandelier_Exit_formula(
                trade_direction, ATR, max(high_prices))
            stop_pips = str(int(abs(float(current_bid) - (ce_stop))))
            print("!!INFO!!...SELL!!")
            print(str(epic_id))
            print(
                "!!INFO!!...Take Profit@...." +
                str(pip_limit) +
                " pips")
        elif trade_direction == "NONE":
            debug_info("Trade direction is NONE")

        # if b_Contrarian:
            # print("!!!WARNING!!! b_Contrarian flag set")
            # print("!!!WARNING!!! b_Contrarian flag set")
            # print("!!!WARNING!!! b_Contrarian flag set")
            # if trade_direction == "SELL":
            # trade_direction == "BUY"
            # elif trade_direction == "BUY":
            # trade_direction == "SELL"
        # else:
            # print("!!!INFO!!! b_Contrarian NOT flag set")
            # print("!!!INFO!!! b_Contrarian NOT flag set")
            # print("!!!INFO!!! b_Contrarian NOT flag set")

        ###############################################################
        ###############################################################
        ########################SANITY CHECKS##########################
        ###############################################################
        ###############################################################

        esma_new_margin_req = int(
            percentage_of(
                ESMA_new_margin,
                current_bid))

        if int(esma_new_margin_req) > int(stop_pips):
            debug_info("ESMA Readjustment....")
            stop_pips = int(esma_new_margin_req)
        if int(pip_limit) == 0:
            debug_info("Pip limit 0!!")  # not worth the trade
            trade_direction = "NONE"
        if int(pip_limit) == 1:
            debug_info("Pip limit 1!!")  # not worth the trade
            trade_direction = "NONE"
        if int(pip_limit) >= int(greed_indicator):
            pip_limit = int(greed_indicator - 1)
        if int(stop_pips) > int(too_high_margin):
            # Remember this "confusing" error
            # message, It's not always too high
            # margin
            debug_info(
                "Got to be junk data OR too_high_margin limit hit!!")
            trade_direction = "NONE"

        #################################################################
        #################################################################
        try_market_order(
            epic_id, trade_direction, pip_limit, stop_pips, positionMap)
        #################################################################
        #################################################################

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print(sys.exc_info()[0])
        debug_info(
            "Something fucked up with the order, or the pricing or whatever!!, Try again!!")
        time.sleep(2)
        pass


def tradeable_epic(epic_id, status):

    try:

        if str(status) == "TRADEABLE":
            ################################
            base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
            auth_r = requests.get(
                base_url, headers=authenticated_headers)
            d = json.loads(auth_r.text)
            #################################
            current_bid = d['snapshot']['bid']
            ask_price = d['snapshot']['offer']
            spread = float(current_bid) - float(ask_price)
            if float(spread) >= spread_check:
                print(
                    "!!INFO!!...FOUND GOOD EPIC..., passing to trade function ..." +
                    str(epic_id))
                time.sleep(1)
                return True
            else:
                print(
                    "!!INFO!!...skipping, NO GOOD EPIC....Checking next epic spreads...")
                time.sleep(1)
                pass
        else:
            print(
                "!!INFO!!...skipping, not tradeable):" +
                str(epic_id))
        time.sleep(0.5)

    except Exception as e:
        # print(e)
        # print(traceback.format_exc())
        # print(sys.exc_info()[0])
        debug_info("bid/ask probably returned NoneType!!!")
        pass


def exploreNode(nodeID):
    base_url = REAL_OR_NO_REAL + '/marketnavigation/' + nodeID
    r = requests.get(base_url, headers=authenticated_headers)

    if isinstance(r.json()['nodes'], list):
        for node in r.json()['nodes']:
            time.sleep(2)
            exploreNode(node['id'])
    if isinstance(r.json()['markets'], list):
        for market in r.json()['markets']:
            # print(market['epic'])

            DFB_TODAY_DAILY_CHECK = [
                "DFB" in str(
                    market['epic']), "TODAY" in str(
                    market['epic']), "DAILY" in str(
                    market['epic'])]

            if any(DFB_TODAY_DAILY_CHECK):
                if tradeable_epic(market['epic'], market['marketStatus']):
                    print("trading.... " + str(market['epic']))
                    no_trade_window()
                    main_trade_function(market['epic'])
            else:
                print(
                    "!!INFO!!...not DFB,TODAY,DAILY!!...." +
                    str(
                        market['epic']))


def no_trade_window():

    while True:

        try:

            base_url = REAL_OR_NO_REAL + "/accounts"
            auth_r = requests.get(base_url, headers=authenticated_headers)
            d = json.loads(auth_r.text)

            # print("--------------Account Info-------------")
            # print("#################DEBUG#################")
            # print(auth_r.status_code)
            # print(auth_r.reason)
            # print(auth_r.text)
            # print("-----------------DEBUG-----------------")
            # print("#################DEBUG#################")

            for i in d['accounts']:
                if str(i['accountType']) == "SPREADBET":
                    balance = i['balance']['balance']
                    deposit = i['balance']['deposit']

            percent_used = percentage(deposit, balance)
            neg_bal_protect = i['balance']['available']

            print("-----------------INFO-----------------")
            print("#################INFO#################")
            print(
                "!!INFO!!...Percent of account used ..." +
                str(percent_used))
            print("-----------------INFO-----------------")
            print("#################INFO#################")

            neg_balance_checks = [
                float(percent_used) > float(acc_used_pct),
                float(neg_bal_protect) < SUPER_LOW_NEG_MARGIN]

            if any(neg_balance_checks):
                print("!!INFO!!...Don't trade, Too much margin used up already")
                time.sleep(60)
                continue
            else:
                debug_info("!!INFO!!...OK to trade...")
                # dont check too often, IG Index API limit 60/min
                time.sleep(3)
                return

        except Exception as e:
            # print(e)
            # print(traceback.format_exc())
            # print(sys.exc_info()[0])
            debug_info("!!ERROR!!...No trade window error!!")
            pass


if __name__ == '__main__':

    debug_info("Program Starting...")

    while True:

        try:

            for t in types.keys():

                try:

                    id, time_zone = types[t]
                    tz = pytz.timezone(time_zone)
                    now_time = datetime.datetime.now(tz=tz).strftime("%H:%M")
                    if is_between(
                        str(now_time),
                        (str(market_close_tm),
                         str(market_open_tm))):
                        print("!!INFO!!...Market Closed, waiting....")
                        timeDelay = random.randrange(0, 90)
                        time.sleep(timeDelay)
                    else:
                        print("!!INFO!!...Market Likely Open")
                        # as not to start again from the start
                        exploreNode(id)
                        no_trade_window()
                except Exception as e:
                    print(e)
                    print(traceback.format_exc())
                    print(sys.exc_info()[0])
                    debug_info("!!ERROR!!...Nothing to see here moving on....")
                    pass

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(sys.exc_info()[0])
            debug_info("!!ERROR!!...Generic Program Error...Moving on!!")
            pass
