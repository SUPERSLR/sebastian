#!/usr/bin/python
# David Newell
# kmldisplay/topobathy/numerical.py
# Display KML features in Google Earth
# Numerical Topography/Bathymetry

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


def buildKML(ge_key=""):
	# Start building elevation data KML
	kml = ''
	
	# Link to SRTM 30 Plus Elevation Data
	kml += '<NetworkLink id="SRTM30PlusTopoBathyLink">\n'
	kml += '<name>SRTM 30 Plus Elevation Data</name>\n'
	kml += '<visibility>1</visibility>\n'
	kml += '<open>0</open>\n'
	kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
	kml += '<description>Data derived from SRTM30_Plus dataset provided by UCSD.</description>\n'
	kml += '<Link>\n'
	kml += '<href>%s/kmldisplay/topobathy/srtm30plus.py</href>\n' % (BASE_URL,)
	kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
	kml += '<viewRefreshTime>3</viewRefreshTime>\n'
	kml += '<viewBoundScale>1.2</viewBoundScale>\n'
	kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
	kml += '</Link>\n'
	kml += '</NetworkLink>\n'
	
	# Link to USGS Elevation Data
	kml += '<NetworkLink id="USGSTopoBathyLink">\n'
	kml += '<name>USGS Elevation Data</name>\n'
	kml += '<visibility>0</visibility>\n'
	kml += '<open>0</open>\n'
	kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
	kml += '<description>Data derived from NGDC 3 Second Coastal Relief Model.</description>\n'
	kml += '<Link>\n'
	kml += '<href>%s/kmldisplay/topobathy/usgs.py</href>\n' % (BASE_URL,)
	kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
	kml += '<viewRefreshTime>3</viewRefreshTime>\n'
	kml += '<viewBoundScale>1.2</viewBoundScale>\n'
	kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
	kml += '</Link>\n'
	kml += '</NetworkLink>\n'
	
	# Link to Google Elevation Data
	kml += '<NetworkLink id="GoogleTopoBathyLink">\n'
	kml += '<name>Google Elevation Data</name>\n'
	kml += '<visibility>0</visibility>\n'
	kml += '<open>0</open>\n'
	kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
	kml += '<description>Data derived from Google\'s Elevation Data Web Service.</description>\n'
	kml += '<Link>\n'
	kml += '<href>%s/kmldisplay/topobathy/google.py</href>\n' % (BASE_URL,)
	kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
	kml += '<viewRefreshTime>3</viewRefreshTime>\n'
	kml += '<viewBoundScale>1.2</viewBoundScale>\n'
	kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
	kml += '</Link>\n'
	kml += '</NetworkLink>\n'

	# Return KML output
	return kml


# If file called directly, output KML
if __name__ == "__main__":
	# Import cgi module to get query string
	import cgi
	
	try:
		# Get query string
		qv = cgi.FieldStorage()
	except:
		qv["GE_KEY"] = ''
	
	# Get user name
	try:
		ge_key = qv["GE_KEY"].value
	except:
		ge_key = ''
	
	# Print content-type header
	print GeoUtils.Interface.ContentType("kml")
	print 
    
	print GeoUtils.Interface.StdKML(buildKML(ge_key=str(ge_key)))
    
    
