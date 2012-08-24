#!/usr/bin/python
# Ben Pedrick
# countries.py
# Summary of resource data by country

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


# Returns and html table summarizing resource information for each country
def getSummary():

	DBhandle = GeoUtils.RDB()
	DBhandle.connect('uws_ge')

	data, rowCount = DBhandle.query('SELECT name, cement, gravel, sand, coastal_engineers, specialty_ships, tugs FROM countries')

	output = ""

	output += '<style type="text/css">\ntable {\n'+\
			'border: 1px solid black;\nborder-collapse: collapse}\n' +\
			'td {\npadding: 3px;\nborder: 1px solid black;}\n' +\
			'th {\npadding: 3px;}\n' +\
			'</style>\n'

	output += '<h2>Country Database Summary</h2>\n'
	output += '<p>This table shows the information we have for each country. ' +\
			'Please help us fill in the blanks! If you have information ' +\
			'we don\'t, find the country marker in Google Earth to ' +\
			'edit the database.</p>\n'
	output += '<p>Cement, Sand, and Gravel production are all in 1000 metric tons per year.</p>\n'

	output += '<table class="sortable">\n<tr><th>Name</th><th>Cement Production</th><th>Gravel Production</th>' +\
			'<th>Sand Production</th><th>Coastal Engineers</th>' +\
			'<th>Speicalty Ships</th><th>Tugs</th></tr>\n'

	#for country in data:
	output += ''.join( [ '<tr><td>%(name)s</td><td>%(cement)s</td><td>%(gravel)s</td><td>%(sand)s</td><td>%(coastal_engineers)s</td><td>%(specialty_ships)s</td><td>%(tugs)s</td></tr>\n' % country for country in data ] )
	
	output += '</table>\n'

	output += '<p></p>' # for spacing

	output += GeoUtils.Interface.buildButton('Completion Status', 'lens', '/sebastian/interface/info/status.py', {})


	return output

if __name__ == "__main__":
	print GeoUtils.Interface.ContentType('html')
	print

	print GeoUtils.Interface.StdHTML(GeoUtils.Interface.uniForm.HTMLHeaderInfo(), getSummary())
