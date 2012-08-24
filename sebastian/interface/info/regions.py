#!/usr/bin/python
# Ben Pedrick
# regions.py
# Launch point to get region summaries

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


def defaultView(dummy, dummy2):
	output = ''

	output += '<h2>Region Information</h2>\n'
	output += '<p>How much concrete will the world need? How much will it all cost? Select an option below to find out.</p>'
	output += '<h3>Choose a Region</h3>\n'
	output += '<a href="/sebastian/interface/info/regions.py?region=world">The World</a>'

	#get all resource names
	DBhandle = GeoUtils.RDB()
	DBhandle.connect('uws_ge')

	names, count = DBhandle.query('SELECT DISTINCT region, sub_region FROM countries')

	DBhandle.close()

	# make sorted list of parents. Remove duplicates by placing into a set and converting back to a list.
	parents = sorted(list(set([row.get('region') for row in names])))

	output += '<ul>\n'
	for p in parents:
		output += '<li>' + regionLink(p,'', p) + '\n<ul>\n'

		# print each subregion as an html sublist
		for subregion in sorted([row.get('sub_region') for row in names if row.get('region') == p]):
			output += '<li>' + regionLink(p, subregion, subregion) + '</li>\n'

		output += '</ul>\n</li>\n'
	
	output += '</ul>\n'

	output += GeoUtils.Interface.buildButton('Information Home', 'lens', '/sebastian/interface/info/intro.py', {})

	return output

def regionView(region, subregion):
	output = ''

	name = ''
	if subregion != '':
		name += subregion
	elif region != '' and region != 'world':
		name += region
	else:
		name = 'the World'

	output += '<h2>Information for ' + name + '</h2>\n'

	output += '<p>So you want to learn something about ' + name + '. ' +\
			'What did you have in mind?'
	
	output += GeoUtils.Interface.buildButton('Resources', 'lens', '/sebastian/interface/info/resources.py', {'region': region, 'subregion' : subregion})
	output += GeoUtils.Interface.buildButton('Cost and Labor', 'lens', '/sebastian/interface/info/costandlabor.py', {'region': region, 'subregion' : subregion})
	output += '<p></p>' # just for spacing
	output += GeoUtils.Interface.buildButton('Select a New Region', 'lens', '/sebastian/interface/info/regions.py', {})

	return output

def regionLink(region, subregion, text):
	output = '<a href="sebastian/interface/info/regions.py?region=' + str(region) + '&subregion=' + str(subregion) + '">' + str(text) + '</a>\n'

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
	else:
		view = 'region'

	print GeoUtils.Interface.StdHTML(GeoUtils.Interface.uniForm.HTMLHeaderInfo(),viewTypes.get(view)(region, subregion))
