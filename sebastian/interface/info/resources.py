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
	output += '<p>It looks like you\'re trying to find resources information, but we ' +\
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
		query += ' WHERE region = "%s"' % (region,)
		if subregion != '':
			query += ' AND sub_region = "%s"' % (subregion,)

	regionInfo, rowCount = DBhandle.query(query)

	if rowCount == 0:
		# no info, print error
		nameText = '""'
		if region != '':
			if subregion != '':
				nameText = '"%s" in "%s"' % (subregion,region)
			else:
				nameText = '"%s"' % (region,)

		output += '<h2>Region not found</h2>\n'
		output += '<p>There was a problem with the page. The region "%s' % (nameText,)
		output += '" is not in our system. If you believe you received this '
		output += 'message in error please contact us at %s.</p>\n' % (GeoUtils.constants.contactEmail,)
		output += GeoUtils.Interface.buildButton('Select a New Region', 'lens', '/sebastian/interface/info/regions.py', {})
		return output

	query = 'SELECT dike_volume, core_volume, toe_volume, foundation_volume, armor_volume, portID '+\
			'FROM portprotector LEFT JOIN portdata ON portprotector.portID = portdata.ID LEFT JOIN '+\
			'countries ON portdata.country = countries.name'

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

	totalVolume = dikeVol + coreVol + toeVol + foundVol + armorVol

	tugs = [c['conversion_factor'] for c in conversions if c['name'] == 'tugsPerVolume'][0] * totalVolume
	specialtyShips = [c['conversion_factor'] for c in conversions if c['name'] == 'specialtyShipsPerVolume'][0] * totalVolume
	coastalEngineers = [c['conversion_factor'] for c in conversions if c['name'] == 'coastalEngineersPerVolume'][0] * totalVolume

	# foundation and core are made of concrete
	concreteVolume = foundVol + coreVol

	# toe and dike are made of fill
	fillVolume = toeVol+ dikeVol

	# armor made of riprap
	riprapVolume = armorVol

	# Get amount of each component needed, multiply by density to get mass, divide by 1000 to get metric tons, and divide by 1000 again
	cementNeeded = concreteVolume * [c['conversion_factor'] for c in conversions if c['name'] == 'cementInConcrete'][0] * \
			[c['conversion_factor'] for c in conversions if c['name'] == 'cementDensity'][0] / 1000. / 1000.
	gravelNeeded = concreteVolume * [c['conversion_factor'] for c in conversions if c['name'] == 'coarseAggregateInConcrete'][0] * \
			[c['conversion_factor'] for c in conversions if c['name'] == 'coarseAggregateDensity'][0] / 1000. / 1000.
	sandNeeded = concreteVolume * [c['conversion_factor'] for c in conversions if c['name'] == 'fineAggregateInConcrete'][0] * \
			[c['conversion_factor'] for c in conversions if c['name'] == 'sandDensity'][0] / 1000. / 1000.

	cementProduction = sum([row['cement'] for row in regionInfo])
	gravelProduction = sum([row['gravel'] for row in regionInfo])
	sandProduction = sum([row['sand'] for row in regionInfo])

	tugsAvailable = sum([row['tugs'] for row in regionInfo])
	specialtyShipsAvailable = sum([row['specialty_ships'] for row in regionInfo])
	coastalEngineersAvailable = sum([row['coastal_engineers'] for row in regionInfo])

	# for formatting numbers
	import locale
	locale.setlocale(locale.LC_ALL, 'en_US')

	cementYears = ''
	if cementProduction != 0:
		cementYears = locale.format('%.2f', cementNeeded / cementProduction, True)
	else:
		cementYears = 'Forever!'

	sandYears = ''
	if sandProduction != 0:
		sandYears = locale.format('%.2f', sandNeeded / sandProduction, True)
	else:
		sandYears = 'Forever!'

	gravelYears = ''
	if gravelProduction != 0:
		gravelYears = locale.format('%.2f', gravelNeeded / gravelProduction, True)
	else:
		gravelYears = 'Forever!'

	# have data - print it out
	output += '<h2>Resources in '
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

	# now write table
	output += '<table>\n<tr><th>Resource</th><th>Available</th><th>Amount Needed</th><th>Years Needed at Current Production</tr>\n'
	output += '<tr><td>Cement</td><td>' + locale.format('%d', cementProduction, True) + \
			' (1000 metric tons produced per year)</td><td>' + locale.format('%d', cementNeeded, True) + ' (1000 metric tons)</td>' +\
			'<td>' + cementYears + '</td></tr>\n'
	output += '<tr><td>Sand</td><td>' + locale.format('%d', sandProduction, True) + \
			' (1000 metric tons produced per year)</td><td>' + locale.format('%d', sandNeeded, True) + ' (1000 metric tons)</td>' +\
			'<td>' + sandYears + '</td></tr>\n'
	output += '<tr><td>Gravel</td><td>' + locale.format('%d', gravelProduction, True) + \
			' (1000 metric tons produced per year)</td><td>' + locale.format('%d', gravelNeeded, True) + ' (1000 metric tons)</td>' +\
			'<td>' + gravelYears + '</td></tr>\n'
	output += '<tr><td>Coastal Engineers</td><td>' + locale.format('%d', sum([row['coastal_engineers'] for row in regionInfo]), True) +\
			' (total engineers)</td><td>' + locale.format('%d', coastalEngineers, True) + ' (engineer years)</td><td>N/A</td></tr>\n'
	output += '<tr><td>Specialty Ships</td><td>' + locale.format('%d', sum([row['specialty_ships'] for row in regionInfo]), True) +\
			' (total ships)</td><td>' + locale.format('%d', specialtyShips, True) + ' (ship years)</td><td>N/A</td></tr>\n'
	output += '<tr><td>Tug Boats</td><td>' + locale.format('%d', sum([row['tugs'] for row in regionInfo]), True) +\
			' (total ships)</td><td>' + locale.format('%d', tugs, True) + ' (ship years)</td><td>N/A</td></tr>\n'
	output += '</table>\n'

	output += '<p></p>' # for spacing
	regionLink = region if region != '' else 'world'
	output += GeoUtils.Interface.buildButton('Back to Region', 'lens', '/sebastian/interface/info/regions.py', {'region': regionLink, 'subregion': subregion})

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
