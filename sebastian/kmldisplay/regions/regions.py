#!/usr/bin/python
# Ben Pedrick
# kmldisplay/regions/regions.py
# Display Placemarkers for regions

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


def KMLout(ge_key=""):
	DBhandle = GeoUtils.RDB()
	DBhandle.connect('uws_ge')

	regions, count = DBhandle.query('SELECT ID, sub_region, longitude, latitude FROM regions')

	output = '<Folder id="Regions">\n'
	output += '<styleUrl>%s/kml_styles.py#check-hide-children</styleUrl>\n' % (BASE_URL,)
	output += '<name>Region Info</name><open>0</open><visibility>1</visibility>\n'

	for r in regions:
		id = str(r.get('ID'))
		name = r.get('sub_region')
		lat = str(r.get('latitude'))
		long = str(r.get('longitude'))
		output += '<Placemark id="Region-%s"><name>%s</name>\n' % (id,name)
		output += '<styleUrl>%s/kml_styles.py#RegionPlacemark</styleUrl>\n' % (BASE_URL,)
		output += '<description><![CDATA['

		output += '<iframe src="%s/interface/main.py?item=Region-%s&amp;GE_KEY=%s" width="400" height="500"></iframe>' % (BASE_URL,id,ge_key)

		output += ']]></description>\n'
		
		output += '<Point><coordinates>%s,%s,0</coordinates></Point>\n' % (long,lat)
		output += '<LookAt><longitude>%s</longitude><latitude>%s</latitude><range>30000</range></LookAt>' % (long,lat)

		output += '</Placemark>\n'

	output += '</Folder>'

	return output

# If file called directly, output kml
if __name__ == "__main__":
	# Print content-type header
	print GeoUtils.Interface.ContentType("kml")
	print 
	
	# Retrieve user information
	qv = []
	
	# Import cgi module to get query string
	import cgi
	
	try:
		# Get query string
		qv = cgi.FieldStorage()
		
		# Get user name
		try:
			ge_key = qv["GE_KEY"].value
		except:
			ge_key = ''
	except:
		ge_key = ''
	
	
	
	print GeoUtils.Interface.StdKML(KMLout(ge_key=str(ge_key)))

