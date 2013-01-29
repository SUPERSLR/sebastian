#!/usr/bin/python
# Ben Pedrick
# resources.py
# Gives the status of resources needed

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


def defaultView(dummy, dummy2):
	output = ''

	output += '<h2>Oops! We forgot what we were looking for.</h2>\n'
	output += '<p>It looks like you\'re trying to find information about costs and labor, but we ' +\
			'don\'t know which part of the world you were interested in.</p>'
	
	output += GeoUtils.Interface.buildButton('Select a New Region', 'lens', '/sebastian/interface/info/regions.py', {})
	output += GeoUtils.Interface.buildButton('Information Home', 'lens', '/sebastian/interface/info/intro.py', {})

	return output

def regionView(region, subregion):
	output = ''

	DBhandle = GeoUtils.RDB()
	DBhandle.connect('uws_ge')

	query = 'SELECT cement, sand, gravel, coastal_engineers, specialty_ships, tugs FROM countries'
	# build query
	if region != '':
		query += ' WHERE region = "' + region + '"'
		if subregion != '':
			query += ' AND sub_region = "' + subregion + '"'

	regionInfo, rowCount = DBhandle.query(query)

	if rowCount == 0:
		# no info, print error
		nameText = '""'
		if region != '':
			if subregion != '':
				nameText = '"' + subregion + '" in "' + region + '"'
			else:
				nameText = '"' + region + '"'

		output += '<h2>Region not found</h2>\n'
		output += '<p>There was a problem with the page. The region "%s" is not in our system. If you believe you received this message in error please contact us at %s.</p>\n' % (nameText,GeoUtils.constants.contactEmail)
		output += GeoUtils.Interface.buildButton('Select a New Region', 'lens', '/sebastian/interface/info/regions.py', {})
		return output

	query = 'SELECT dike_volume, core_volume, toe_volume, foundation_volume, armor_volume, portID FROM portprotector LEFT JOIN portdata ' +\
		'ON portprotector.portID = portdata.ID LEFT JOIN countries ON ' +\
		'portdata.country = countries.name'

	if region != '':
		query += ' WHERE countries.region="%s"' % (region,)
		if subregion != '':
			query += ' AND countries.sub_region="%s"' % (subregion,)

	# get all volumes
	dikes, rowCount = DBhandle.query(query)

	dikeVol = 0.0
	coreVol = 0.0
	toeVol = 0.0
	foundVol = 0.0
	armorVol = 0.0

	ports = set()
	# sum up total volumes for region
	for d in dikes:
		# only count one path per port
		if d['portID'] not in ports:
			ports.add(d['portID'])
			dikeVol += d['dike_volume']
			coreVol += d['core_volume']
			toeVol += d['toe_volume']
			foundVol += d['foundation_volume']
			armorVol += d['armor_volume']

	# get conversion factors from database
	conversions, rowCount = DBhandle.query('SELECT name, conversion_factor FROM conversions')

	cost = {'dike': dikeVol * [c['conversion_factor'] for c in conversions if c['name'] == 'dikeCost'][0],
			'core': coreVol * [c['conversion_factor'] for c in conversions if c['name'] == 'coreCost'][0],
			'found': foundVol * [c['conversion_factor'] for c in conversions if c['name'] == 'foundationCost'][0], 
			'toe': toeVol * [c['conversion_factor'] for c in conversions if c['name'] == 'toeCost'][0],
			'armor': armorVol * [c['conversion_factor'] for c in conversions if c['name'] == 'armoringCost'][0],
			}

	labor = {'dike': dikeVol * [c['conversion_factor'] for c in conversions if c['name'] == 'dikeLabor'][0],
			'core': coreVol * [c['conversion_factor'] for c in conversions if c['name'] == 'coreLabor'][0],
			'found': foundVol * [c['conversion_factor'] for c in conversions if c['name'] == 'foundationLabor'][0], 
			'toe': toeVol * [c['conversion_factor'] for c in conversions if c['name'] == 'toeLabor'][0],
			'armor': armorVol * [c['conversion_factor'] for c in conversions if c['name'] == 'armoringLabor'][0],
			}

	# have data - print it out
	output += '<h2>Costs and Labor for '
	if subregion != '':
		output += subregion
	elif region != '':
		output += region
	else:
		output += 'the World'
	output += '</h2>\n'
	
	# style table
	output += '<style type="text/css">\ntable {\n'+\
			'border: 1px solid black;\nborder-collapse: collapse}\n' +\
			'td {\npadding: 3px;\nborder: 1px solid black;}\n' +\
			'th {\npadding: 3px;}\n' +\
			'</style>\n'

	output += '<p>The construction time assumes a crew of 20 working 50 40-hour weeks a year.</p>'

	import locale
	locale.setlocale(locale.LC_ALL, 'en_US') # this formats values nicely for printing

	# now write table
	output += '<table class="sortable">\n<thead>\n<tr><th>Component</th><th>Labor</th><th>Cost</th><th>Construction Time</th></tr>\n</thead>\n<tbody>\n'
	output += '<tr><td>Armor</td><td>' + locale.format('%d', labor['armor'], True) + ' man-hours</td><td>$' +\
			locale.format('%.2f', cost['armor'], True) +\
			'</td><td>' + locale.format('%.2f', labor['armor'] / 20 / 40 / 50, True) + ' years</td></tr>'
	output += '<tr><td>Core</td><td>' + locale.format('%d', labor['core'], True) + ' man-hours</td><td>$' +\
			locale.format('%.2f', cost['core'], True) +\
			'</td><td>' + locale.format('%.2f', labor['core'] / 20 / 40 / 50, True) + ' years</td></tr>'
	output += '<tr><td>Dike</td><td>' + locale.format('%d', labor['dike'], True) + ' man-hours</td><td>$' +\
			locale.format('%.2f', cost['dike'], True) +\
			'</td><td>' + locale.format('%.2f', labor['dike'] / 20 / 40 / 50, True) + ' years</td></tr>'
	output += '<tr><td>Foundation</td><td>' + locale.format('%d', labor['found'], True) + ' man-hours</td><td>$' +\
			locale.format('%.2f', cost['found'], True) +\
			'</td><td>' + locale.format('%.2f', labor['found'] / 20 / 40 / 50, True) + ' years</td></tr>'
	output += '<tr><td>Toe</td><td>' + locale.format('%d', labor['toe'], True) + ' man-hours</td><td>$' +\
			locale.format('%.2f', cost['toe'], True) +\
			'</td><td>' + locale.format('%.2f', labor['toe'] / 20 / 40 / 50, True) + ' years</td></tr>'
	output += '</tbody>\n<tfoot><tr><td>Total</td><td>' + locale.format('%d', sum([value for key, value in labor.items()]), True) + \
			' man-hours</td><td>$' + locale.format('%.2f', sum([value for key, value in cost.items()]), True) +\
			'</td><td>' + locale.format('%.2f', sum([value for key, value in labor.items()]) / 20 / 40 / 50, True) + ' years</td></tr>\n</table>\n'

	# if region is blank, where getting the whole world
	regionName = region if region != '' else 'world'
	output += '<p></p>' # for spacing
	output += GeoUtils.Interface.buildButton('Back to Region', 'lens', '/sebastian/interface/info/regions.py', {'region': regionName, 'subregion': subregion})

	DBhandle.close()

	return output

if __name__ == "__main__":
	print GeoUtils.Interface.ContentType("html")
	print

	# Retrieve params
	qv = []
	import cgi

	qv = cgi.FieldStorage()

	try:
		region = str(qv["region"].value)
		try:
			subregion = str(qv["subregion"].value)
		except KeyError:
			# if subregion is not filled in, just leave it blank.
			# it's ok to only have region filled.
			subregion = ''

		error = 'None'
	except KeyError:
		region = ''
		subregion = ''
		error = KeyError
	
	viewTypes = {
			"default" : defaultView,
			"world" : regionView,
			"region" : regionView}

	if region == '':
		view = 'default'
	elif region == 'world':
		view = 'world'
		region = '' # this tells the region view to get the whole world
	else:
		view = 'region'

	print GeoUtils.Interface.StdHTML(GeoUtils.Interface.uniForm.HTMLHeaderInfo(),viewTypes.get(view)(region, subregion))
