#!/usr/bin/env python

import sys
import json
import requests

API_URL = 'http://query.yahooapis.com/v1/public/yql'
BASE_PARAMS = {
		'format': 'json',
		'env': 'store://datatables.org/alltableswithkeys'
}


def quotes( symbols ):
	'''
	Gets quotes

	Args:
		quotes (string): comma-separated list of ticker symbols
	Returns:
		Dictionary of quotes
	'''
	query = BASE_PARAMS.copy()
	s = ', '.join('"%s"' % i for i in symbols)
	query['q'] = 'select * from yahoo.finance.quotes where symbol in (%s)' % s

	r = requests.get( API_URL, params=query )
	quotes = r.json()['query']['results']['quote']
	return quotes

def xchange( currencies ):
	'''

	'''

def prettify( data ):
	print json.dumps(data, sort_keys=True, indent=4)


def main():
	if len(sys.argv) < 2:
		sys.exit('You forgot to pass an argument')
	arg = sys.argv[1]

	results = quotes( arg )

	if not results:
		sys.exit(1)

	prettify(results)

	return 0

def ribosome(targets, results):
	target = targets.pop(0)
	if target.endswith(FILE_FORMATS):
		if not results.has_key('books'): results['books'] = []
		results['books'].append(target)
	else:
		if not results.has_key(target): results[target] = {}
		return ribosome(targets, results[target])
	return results


if __name__ == '__main__':
	sys.exit(main())