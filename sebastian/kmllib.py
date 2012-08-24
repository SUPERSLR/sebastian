#!/usr/bin/python
# David Newell
# kmllib.py
# Underwatershipping.com KML library generation

BASE_PATH = "/home/jack_sparrow/sebastian.sp/sebastian/"

# Import Useful Modules
import sys
sys.path.append(BASE_PATH)
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL



# Cache controls
# "Cache-Control: no-cache, must-revalidate\n"
#print "Expires: Mon, 26 Jul 1997 05:00:00 GMT\n\n"


# If called directly, run
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
	
	
	# ------------------------------------------------------
	# Begin KML Output
	# ------------------------------------------------------
	
	
	# KML Header
	kml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
	kml_output += '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
	
	# Start document of network links
	kml_output += '<Document>'
	
	kml_output += '<NetworkLink id="sebastian">\n'
	kml_output += '<name>Sebastian GeoData System</name>\n'
	kml_output += '<visibility>0</visibility>\n'
	kml_output += '<open>0</open>\n'
	kml_output += '<description><span style="color:blue"><strong>OPERATIONAL</strong></span></description>\n'
	kml_output += '<Link>\n'
	kml_output += '<href>%s/geodata-display.py</href>\n' % (BASE_URL,)
	kml_output += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
	kml_output += '</Link>\n'
	kml_output += '</NetworkLink>\n'
	
	# Close document
	kml_output += '</Document>'
	
	# End of kml file
	kml_output += '</kml>'
	
	# Display kml file
	print kml_output

