#!/usr/bin/env python

'''
	Stocker 0.1.0
	By Francis Tseng
	frnsys.com / @frnsys

	A Python wrapper for the Yahoo Finance API
	With many thanks to http://goo.gl/gSEmw
'''

import sys
import requests
import json
from datetime import datetime

props = json.loads( open('properties.json').read() )
QUOTE_PROPS = props['quotes']
INDUSTRIES = props['industries']
COMPANIES = props['companies']

def quotes( symbols, props=[] ):
	'''
	Gets quotes

	Args:
		symbols (list): list of ticker symbols
		props (list): list of props to collect
	Returns:
		List of quote data
		[{label:value}]
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

	results = {}
	for i, row in enumerate(r.text.strip().split('\n')):
		data = [datum.replace('"','').strip() for datum in row.split(',')]
		results[symbols[i]] = dict(zip(props,data))
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
		dict of symbols with their data
		{symbol:{label:value}}
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
		results[symbol] = _fetch( url )
	return results

def sectors( sort_up=True ):
	'''
	Gets data for all sectors

	Args:
		sort (bool): sort up or down
	Returns:
		list of dicts of sector data
	'''

	api_url = 'http://biz.yahoo.com/p/csv/s_coname'
	sort = 'u' if sort_up else 'd'

	url = api_url + sort + '.csv'
	return _fetch( url )

def industries( industries, sort_up=True ):
	'''
	Gets data for industries

	Args:
		industries (list): list of industry names
		sort (bool): sort up or down
	Returns:
		dict of industries with their data
		{industry:{label:value}}
	'''
	api_url = 'http://biz.yahoo.com/p/csv/'
	sort = 'u' if sort_up else 'd'

	results = {}
	for industry in list(industries):
		if industry not in INDUSTRIES:
			industries.remove(industry)
			continue

		url = api_url + str(INDUSTRIES[industry]) + 'coname' + sort + '.csv'
		results[industry] = _fetch( url )
	return results

def companies( companies, sort_up=True ):
	'''
	Gets data for companies

	Args:
		companies (list): list of company names
		sort (bool): sort up or down
	Returns:
	'''
	api_url = 'http://biz.yahoo.com/p/csv/'
	sort = 'u' if sort_up else 'd'

	results = {}
	for company in list(companies):
		if company not in COMPANIES:
			companies.remove(company)
			continue
		url = api_url + str(COMPANIES[company]) + 'coname' + sort + '.csv'
		results[company] = _fetch( url )
	return results
	

def _fetch( url, params=[] ):
	'''
	fetches CSV data and parses it
	'''
	r = requests.get( url, params=params )
	csv = r.text.split("\n")
	labels = csv.pop(0).replace('"','').split(",")

	results = []
	for row in csv:
		data = [datum.replace('"','').strip() for datum in row.split(",")]
		results.append(dict(zip(labels,data)))
	return results