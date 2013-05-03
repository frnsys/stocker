#!/usr/bin/env python
# With many thanks to http://goo.gl/gSEmw

import sys
import csv
import requests
from datetime import datetime

# Thanks to http://goo.gl/wCyUQ
QUOTE_PROPS = {
			# Pricing
			'ask': 'a',
			'bid': 'b',
			'ask_realtime': 'b2',
			'bid_realtime': 'b3',
			'previous_close': 'p',
			'open': 'o',
			'change': 'c1',
			'change_and_percent_change': 'c',
			'change_realtime': 'c6',
			'change_percent_realtime': 'k2',
			'change_in_percent': 'p2',
			'after_hours_change_realtime': 'c8',
			'commission': 'c3',
			'days_low': 'g',
			'days_high': 'h',
			'last_trade_with_time_realtime': 'k1',
			'last_trade_with_time': 'l',
			'last_trade_price_only': 'l1',
			'one_year_target_price': 't8',
			'days_value_change': 'w1',
			'days_value_change_realtime': 'w4',
			'price_paid': 'p1',
			'days_range': 'm',
			'days_range_realtime': 'm2',

			# 52 Week Pricing
			'52_week_high': 'k',
			'52_week_low': 'j',
			'change_from_52_week_low': 'j5',
			'change_from_52_week_high': 'k4',
			'percent_change_from_52_week_low': 'j6',
			'percent_Change_from_52_week_high': 'k5',
			'52_week_range': 'w',

			# Volume
			'volume': 'v',
			'ask_size': 'a5',
			'bid_size': 'b6',
			'last_trade_size': 'k3',
			'average_daily_volume': 'a2',

			# Ratios
			'eps': 'e',
			'eps_estimate_current_year': 'e7',
			'eps_estimate_next_year': 'e8',
			'eps_estimate_next_quarter': 'e9',
			'book_value': 'b4',
			'ebitda': 'j4',
			'price_to_sales': 'p5',
			'price_to_book': 'p6',
			'pe_ratio': 'r',
			'pe_ratio_realtime': 'r2',
			'peg_ratio': 'r5',
			'price_to_eps_estimate_current_year': 'r6',
			'price_to_eps_estimate_next_year': 'r7',
			'short_ratio': 's7',

			# Dividends
			'dividend_yield': 'y',
			'dividend_per_share': 'd',
			'dividend_pay_date': 'r1',
			'ex_dividto_date': 'q',

			# Date
			'last_trade_date': 'd1',
			'trade_date': 'd2',
			'last_trade_time': 't1',

			# Averages
			'change_from_200_day_moving_average': 'm5',
			'percent_change_from_200_day_moving_average': 'm6',
			'change_from_50_day_moving_average': 'm7',
			'percent_change_from_50_day_moving_average': 'm8',
			'50_day_moving_average': 'm3',
			'200_day_moving_average': 'm4',

			# Misc
			'holdings_gain_percent': 'g1',
			'annualized_gain': 'g3',
			'holdings_gain': 'g4',
			'holdings_gain_percent_realtime': 'g5',
			'holdings_gain_realtime': 'g6',

			# Symbol Info
			'more_info': 'v',
			'market_cap': 'j1',
			'market_cap_realtime': 'j3',
			'float_shares': 'f6',
			'name': 'n',
			'notes': 'n4',
			'symbol': 's',
			'shares_owned': 's1',
			'stock_exchange': 'x',

			# Misc
			'ticker_trend': 't7',
			'trade_links': 't6',
			'order_book_realtime': 'i5',
			'high_limit': 'l2',
			'low_limit': 'l3',
			'holdings_value': 'v1',
			'holdings_value_realtime': 'v7'
		}


def quotes( symbols, properties=[] ):
	'''
	Gets quotes

	Args:
		symbols (list): list of ticker symbols
		properties (list): list of properties to collect
	Returns:
		List of quotes
	'''
	api_url = 'http://download.finance.yahoo.com/d/quotes.csv'

	if not properties: properties = QUOTE_PROPS.keys()
	f = [QUOTE_PROPS[p]
			for p in properties
			if p in QUOTE_PROPS]

	params = {
				'f': ''.join(f),
				's': ','.join(symbols),
				'e': '.csv'
			}

	r = requests.get( api_url, params=params )

	results = []
	for row in r.text.split('\n'):
		data = [datum.replace('"','').strip() for datum in row.split(',')]
		results.append(dict.zip(properties,data))
	return results

def history( symbols, from_date, to_date, interval ):
	'''
	Gets historical stock/index quote data

	Args:
		symbols (list): list of ticker symbols
		from_date (string): date in the format mm/dd/yyyy
		to_date (string): date in the format mm/dd/yyyy
		interval (string): trading interval (d=daily, w=weekly, m=monthly, v=dividends)
	Returns:
		Dict of symbol:data
	'''
	api_url = 'http://ichart.yahoo.com/table.csv'
	start = datetime.strptime(from_date, "%m/%d/%Y")
	end = datetime.strptime(to_date, "%m/%d/%Y")

	if start > end: return
	if interval not in ['d','w','m','v']: return

	params = {
				'ignore': '.csv',
				'a': start.month - 1,
				'b': start.day,
				'c': start.year,
				'd': end.month - 1,
				'e': end.day,
				'f': end.year,
				'g': interval
			}

	results = {}
	for symbol in symbols:
		_params = params.copy()
		_params['s'] = symbol
		r = requests.get( api_url, params=_params )

		csv = r.text.split("\n")
		labels = csv.pop(0).split(",")

		d = []
		for row in csv:
			data = [datum.strip() for datum in row.split(",")]
			d.append(dict(zip(labels,data)))
		results[symbol] = d

	return results
	


def main():
	if len(sys.argv) < 2:
		sys.exit('You forgot to pass an argument')
	args = sys.argv[1:]

	results = history( args, "3/15/2000", "1/31/2010", 'w' )

	print results['GOOG']

	if not results:
		sys.exit(1)

	return 0


if __name__ == '__main__':
	sys.exit(main())