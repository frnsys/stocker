#!/usr/bin/env python
# With many thanks to http://goo.gl/gSEmw

import sys
import os
import requests
import yaml
from datetime import datetime

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
props = yaml.load(open(os.path.join(__location__, 'properties.yml')))
QUOTE_PROPS = props['quotes']
INDUSTRIES = props['industries']

def quotes( symbols, props=[] ):
	'''
	Gets quotes

	Args:
		symbols (list): list of ticker symbols
		props (list): list of props to collect
	Returns:
		List of quotes
	'''
	api_url = 'http://download.finance.yahoo.com/d/quotes.csv'

	if not props: props = QUOTE_PROPS.keys()
	f = [QUOTE_PROPS[p]
			for p in props
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
		results.append(dict.zip(props,data))
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
	# You can only access one symbol at a time,
	# so we must request each one individually.
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

def sectors( sort='u' ):
	api_url = 'http://biz.yahoo.com/p/csv/s_coname'

	if sort not in ['u','d']: sort = 'u'

	r = requests.get( api_url + sort + '.csv' )
	print r.url
	print r.text

def industries( industry, sort='u' ):
	api_url = 'http://biz.yahoo.com/p/csv/'

	if industry not in INDUSTRIES: return
	if sort not in ['u','d']: sort = 'u'

	url = api_url + str(INDUSTRIES[industry]) + 'coname' + sort + '.csv'
	r = requests.get( url )
	print r.text
	


def main():
	if len(sys.argv) < 2:
		sys.exit('You forgot to pass an argument')
	args = sys.argv[1:]

	#results = history( args, "3/15/2000", "1/31/2010", 'w' )
	#results = sectors()
	results = industries('services')

	if not results:
		sys.exit(1)

	return 0


if __name__ == '__main__':
	sys.exit(main())