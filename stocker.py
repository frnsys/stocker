#!/usr/bin/env python
# With many thanks to http://goo.gl/gSEmw

import sys
import csv
import requests

QUOTE_PROPS = {
			'AfterHoursChangeRealtime': 'c8',
			'AnnualizedGain': 'g3',
			'Ask': 'a0',
			'AskRealtime': 'b2',
			'AskSize': 'a5',
			'AverageDailyVolume': 'a2',
			'Bid': 'b0',
			'BidRealtime': 'b3',
			'BidSize': 'b6',
			'BookValuePerShare': 'b4',
			'Change': 'c1',
			'ChangeChangeInPercent': 'c0',
			'ChangeFromFiftyDayMovingAverage': 'm7',
			'ChangeFromTwoHundredDayMovingAverage': 'm5',
			'ChangeFromYearHigh': 'k4',
			'ChangeFromYearLow': 'j5',
			'ChangeInPercent': 'p2',
			'ChangeInPercentRealtime': 'k2',
			'ChangeRealtime': 'c6',
			'Commission': 'c3',
			'Currency': 'c4',
			'DaysHigh': 'h0',
			'DaysLow': 'g0',
			'DaysRange': 'm0',
			'DaysRangeRealtime': 'm2',
			'DaysValueChange': 'w1',
			'DaysValueChangeRealtime': 'w4',
			'DividendPayDate': 'r1',
			'TrailingAnnualDividendYield': 'd0',
			'TrailingAnnualDividendYieldInPercent': 'y0',
			'DilutedEPS': 'e0',
			'EBITDA': 'j4',
			'EPSEstimateCurrentYear': 'e7',
			'EPSEstimateNextQuarter': 'e9',
			'EPSEstimateNextYear': 'e8',
			'ExDividendDate': 'q0',
			'FiftyDayMovingAverage': 'm3',
			'SharesFloat': 'f6',
			'HighLimit': 'l2',
			'HoldingsGain': 'g4',
			'HoldingsGainPercent': 'g1',
			'HoldingsGainPercentRealtime': 'g5',
			'HoldingsGainRealtime': 'g6',
			'HoldingsValue': 'v1',
			'HoldingsValueRealtime': 'v7',
			'LastTradeDate': 'd1',
			'LastTradePriceOnly': 'l1',
			'LastTradeRealtimeWithTime': 'k1',
			'LastTradeSize': 'k3',
			'LastTradeTime': 't1',
			'LastTradeWithTime': 'l0',
			'LowLimit': 'l3',
			'MarketCapitalization': 'j1',
			'MarketCapRealtime': 'j3',
			'MoreInfo': 'i0',
			'Name': 'n0',
			'Notes': 'n4',
			'OneyrTargetPrice': 't8',
			'Open': 'o0',
			'OrderBookRealtime': 'i5',
			'PEGRatio': 'r5',
			'PERatio': 'r0',
			'PERatioRealtime': 'r2',
			'PercentChangeFromFiftyDayMovingAverage': 'm8',
			'PercentChangeFromTwoHundredDayMovingAverage': 'm6',
			'ChangeInPercentFromYearHigh': 'k5',
			'PercentChangeFromYearLow': 'j6',
			'PreviousClose': 'p0',
			'PriceBook': 'p6',
			'PriceEPSEstimateCurrentYear': 'r6',
			'PriceEPSEstimateNextYear': 'r7',
			'PricePaid': 'p1',
			'PriceSales': 'p5',
			'Revenue': 's6',
			'SharesOwned': 's1',
			'SharesOutstanding': 'j2',
			'ShortRatio': 's7',
			'StockExchange': 'x0',
			'Symbol': 's0',
			'TickerTrend': 't7',
			'TradeDate': 'd2',
			'TwoHundredDayMovingAverage': 'm4',
			'Volume': 'v0',
			'YearHigh': 'k0',
			'YearLow': 'j0',
			'YearRange': 'w0'
		}


def quotes( symbols, properties=[] ) :
	'''
	Gets quotes

	Args:
		symbols (list): list of ticker symbols
		properties (list): list of properties to collect
	Returns:
		Array of quotes
	'''
	api_url = 'http://download.finance.yahoo.com/d/quotes.csv'

	if not properties: properties = QUOTE_PROPS.keys()
	print properties
	f = [QUOTE_PROPS[p]
			for p in properties
			if p in QUOTE_PROPS]

	params = {
				'f': ''.join(f),
				's': ','.join(symbols),
				'e': '.csv'
			}

	r = requests.get( api_url, params=params )
	data = [datum.replace('"','').strip() for datum in r.text.split(',')]
	results = dict(zip(properties, data))

	print results
	return results

def xchange( *currencies ):
	'''

	'''


def main():
	if len(sys.argv) < 2:
		sys.exit('You forgot to pass an argument')
	args = sys.argv[1:]

	results = quotes( args, ['Name', 'Symbol', 'Change'] )
	results = quotes( args )

	if not results:
		sys.exit(1)

	return 0


if __name__ == '__main__':
	sys.exit(main())