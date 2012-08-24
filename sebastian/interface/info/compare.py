#!/usr/bin/python
# Ben Pedrick
# compare.py
# Run some simple comparisons

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

def default():
	output = '<h2>Comparisons</h2>\n<p>Here you can find some interesting ' +\
			'information about how different parts of the world stack up.</p>\n'

	output += GeoUtils.Interface.buildButton('Resource Production', 'lens', '/sebastian/interface/info/compare.py', {'topic' : 'resources'})
	output += GeoUtils.Interface.buildButton('Dikes by Size', 'lens', '/sebastian/interface/info/compare.py', {'topic' : 'paths'})
	output += GeoUtils.Interface.buildButton('Information Home', 'lens', '/sebastian/interface/info/intro.py', {})

	return output

# Prints a comparison of cement, gravel, and sand production
def resources():
	output = '<h2>Resource Production</h2>\n<p>The charts below show the differences ' +\
			'in cement, gravel, and sand production throughout the world.</p>\n'

	DBhandle = GeoUtils.RDB()
	DBhandle.connect('uws_ge')

	info, count = DBhandle.query('SELECT region, sub_region, cement, sand, gravel FROM countries')

	# now order it into a dictionary
	resources = {}
	totals = {'cement' : 0, 'sand' : 0, 'gravel' : 0}

	for i in info:
		if i['region'] not in resources:
			resources[i['region']] = {}
		
		regDict = resources[i['region']]

		if i['sub_region'] not in regDict:
			regDict[i['sub_region']] = {'cement' : 0, 'sand' : 0, 'gravel' : 0}

		subDict = regDict[i['sub_region']]

		subDict['cement'] += i['cement']
		subDict['gravel'] += i['gravel']
		subDict['sand'] += i['sand']
		totals['cement'] += i['cement']
		totals['gravel'] += i['gravel']
		totals['sand'] += i['sand']
	
	# output a concentric pie chart using google charts api
	# regions on the inner part, sub region on the outer part
	output += '<h3>Cement</h3>'
	output += '<img src="http://chart.apis.google.com/chart?cht=pc&chs=600x380&chd=t:'
	innerLabels = []
	for reg in resources:
		innerLabels.append(reg)
		output += str(sum([resources[reg][sub]['cement'] for sub in resources[reg]]) / totals['cement'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# now do sub regions
	output += '|'
	outerLabels = []
	for reg in resources:
		for sub in resources[reg]:
			outerLabels.append(sub)
			output += str(resources[reg][sub]['cement'] / totals['cement'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# add labels
	output += '&chl='
	for name in innerLabels:
		output += name + '|'
	for name in outerLabels:
		output += name + '|'

	# remove trailing |
	output = output[:-1]

	output += '"></img>'
	
	# Now gravel...
	output += '<h3>Gravel</h3>'
	output += '<img src="http://chart.apis.google.com/chart?cht=pc&chs=600x380&chd=t:'
	innerLabels = []
	for reg in resources:
		innerLabels.append(reg)
		output += str(sum([resources[reg][sub]['gravel'] for sub in resources[reg]]) / totals['gravel'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# now do sub regions
	output += '|'
	outerLabels = []
	for reg in resources:
		for sub in resources[reg]:
			outerLabels.append(sub)
			output += str(resources[reg][sub]['gravel'] / totals['gravel'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# add labels
	output += '&chl='
	for name in innerLabels:
		output += name + '|'
	for name in outerLabels:
		output += name + '|'

	# remove trailing |
	output = output[:-1]
	
	output += '"></img>'
	
	# sand
	output += '<h3>Sand</h3>'
	output += '<img src="http://chart.apis.google.com/chart?cht=pc&chs=600x380&chd=t:'
	innerLabels = []
	for reg in resources:
		innerLabels.append(reg)
		output += str(sum([resources[reg][sub]['sand'] for sub in resources[reg]]) / totals['sand'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# now do sub regions
	output += '|'
	outerLabels = []
	for reg in resources:
		for sub in resources[reg]:
			outerLabels.append(sub)
			output += str(resources[reg][sub]['sand'] / totals['sand'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# add labels
	output += '&chl='
	for name in innerLabels:
		output += name + '|'
	for name in outerLabels:
		output += name + '|'

	# remove trailing |
	output = output[:-1]

	output += '"></img>'

	output += '<p></p>' # for spacing
	output += GeoUtils.Interface.buildButton('More Comparisons', 'lens', '/sebastian/interface/info/compare.py', {})

	return output

# show path length and volume by region
def paths():
	output = '<h2>Protector Paths</h2>\n<p>Where in the world is the most work needed?</p>'

	DBhandle = GeoUtils.RDB()
	DBhandle.connect('uws_ge')

	paths, count = DBhandle.query('SELECT portprotector.path_length, portprotector.path_volume, countries.region, ' +\
			'countries.sub_region FROM portprotector LEFT JOIN portdata ' +\
			'ON portprotector.portID = portdata.ID LEFT JOIN countries ' +\
			'ON portdata.country = countries.name')
	
	regions = {}
	totals = { 'length' : 0, 'volume' : 0 }

	for path in paths:
		if path['region'] not in regions:
			regions[path['region']] = {}

		reg = regions[path['region']]

		if path['sub_region'] not in reg:
			reg[path['sub_region']] = { 'length' : 0, 'volume' : 0 }

		sub = reg[path['sub_region']]

		sub['length'] += path['path_length']
		sub['volume'] += path['path_volume']
		totals['length'] += path['path_length']
		totals['volume'] += path['path_volume']

	# output a concentric pie chart using google charts api
	# regions on the inner part, sub region on the outer part
	output += '<h3>Combined Length of Dikes</h3>'
	output += '<img src="http://chart.apis.google.com/chart?cht=pc&chs=600x380&chd=t:'
	innerLabels = []
	for reg in regions:
		innerLabels.append(reg)
		output += str(sum([regions[reg][sub]['length'] for sub in regions[reg]]) / totals['length'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# now do sub regions
	output += '|'
	outerLabels = []
	for reg in regions:
		for sub in regions[reg]:
			outerLabels.append(sub)
			output += str(regions[reg][sub]['length'] / totals['length'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# add labels
	output += '&chl='
	for name in innerLabels:
		output += name + '|'
	for name in outerLabels:
		output += name + '|'

	# remove trailing |
	output = output[:-1]

	output += '"></img>'

	# now by volumes
	output += '<h3>Combined Volume of Dikes</h3>'
	output += '<img src="http://chart.apis.google.com/chart?cht=pc&chs=600x380&chd=t:'
	innerLabels = []
	for reg in regions:
		innerLabels.append(reg)
		output += str(sum([regions[reg][sub]['volume'] for sub in regions[reg]]) / totals['volume'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# now do sub regions
	output += '|'
	outerLabels = []
	for reg in regions:
		for sub in regions[reg]:
			outerLabels.append(sub)
			output += str(regions[reg][sub]['volume'] / totals['volume'] * 100) + ','

	# remove trailing ,
	output = output[:-1]

	# add labels
	output += '&chl='
	for name in innerLabels:
		output += name + '|'
	for name in outerLabels:
		output += name + '|'

	# remove trailing |
	output = output[:-1]

	output += '"></img>'

	output += '<p></p>' # for spacing
	output += GeoUtils.Interface.buildButton('More Comparisons', 'lens', '/sebastian/interface/info/compare.py', {})

	return output


if __name__ == '__main__':
	print GeoUtils.Interface.ContentType('html')
	print

	import cgi
	qv = cgi.FieldStorage()

	try:
		topic = str(qv['topic'].value)
	except KeyError:
		topic = 'default'

	pages = { 'default' : default,
			'resources' : resources,
			'paths' : paths
			}

	print GeoUtils.Interface.StdHTML(GeoUtils.Interface.uniForm.HTMLHeaderInfo(), pages[topic]())
