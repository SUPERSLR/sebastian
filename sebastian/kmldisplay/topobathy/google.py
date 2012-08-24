#!/usr/bin/python
# David Newell
# kmldisplay/topobathy/google.py
# Display KML features in Google Earth
# Google Numerical Topography/Bathymetry

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Connect to database
DBhandle = GeoUtils.RDB()
#DBhandle.setHost(GeoUtils.constants.AmazonHost)
DBhandle.connect('uws_ge')



def KMLout(bbox=["-74.4","40.4","-73.5","40.9"],ge_key=""):
	# Database table information
	table = 'elev_data'
	
	# Get BBOX boundaries
	west = float(bbox[0])
	east = float(bbox[2])
	north = float(bbox[3])
	south = float(bbox[1])
	
	# Set default center of view
	center_lon = '0'
	center_lat = '0'
	
	# Calculate the height and width of view
	height = north - south
	width = east - west
	
	# If view is shorter than .5 degrees or narrower than .8 degrees, show grid, otherwise, don't
	if abs(height) < .5 or abs(width) < .8:
		show_grid = True
	else:
		show_grid = False
	
	# Find the center point of view
	center_lon = width / 2 + west
	center_lat = height / 2 + south
    
	
	# -----------------------------------------------
	#
	# Google Web Service (mostly 3 arc-second)
	#
	# -----------------------------------------------

	# KML Header
	kml_output = '<Folder id="GoogleTopoBathy">\n'
	kml_output += '<styleUrl>%s/kml_styles.py#check-hide-children</styleUrl>\n' % (BASE_URL,)
	kml_output += '<name>Google Numerical Topography-Bathymetry</name><open>0</open><visibility>1</visibility>\n'
	kml_output += '<description>Data derived from Google\'s Elevation Data Web Service.</description>\n'
	
	# Use a narrower view for this one...
	# If view is shorter than .05 degrees or narrower than .08 degrees, show grid, otherwise, don't
	if abs(height) < .05 or abs(width) < .08:
		show_grid = True
	else:
		show_grid = False
	
	
	# If zoomed in enough to view grid, query db and display data
	if show_grid:
		# Database query
		dbq = "SELECT longitude,latitude,elevation FROM %s WHERE " % (table,)
		dbq += "longitude <= %s AND longitude >= %s AND " % (east,west)
		dbq += "latitude <= %s AND latitude >= %s" % (north,south)
		dbq += " AND source='google_web_service'"
		
		# Query database
		dbdata,rowcount = DBhandle.query(dbq)
		
		# Close database
		DBhandle.close()
		
		# If there are results from the database, show grid
		if rowcount > 0:
			
			for r in dbdata:
				# Create placemark with elevation as name
				kml_output += '<Placemark><name>%s</name>\n' % (r["elevation"],)
				kml_output += '<styleUrl>%s/kml_styles.py#depthPoint</styleUrl>\n' % (BASE_URL,)
				kml_output += '<Point>\n'
				kml_output += '<coordinates>%(longitude)s,%(latitude)s,0</coordinates>\n' % r
				kml_output += '</Point>\n'
				kml_output += '</Placemark>\n'
		
		# If no results from database, show error placemark
		else:
			kml_output += '<Placemark><name>No Data</name><description>There was an error with your request. Please try again!</description><styleUrl>%s/kml_styles.py#error_placemark</styleUrl><Point><coordinates>' % (BASE_URL,)
			kml_output += '%s,%s,0' % (center_lon,center_lat)
			kml_output += '</coordinates></Point></Placemark>'
	
	
	# If grid is not shown, zoom in placemark
	else:
		# Zoom in placemark KML with coordinates at center point -- displays number of results at that zoom level in description balloon
		kml_output += '<Placemark><name>Zoom in</name><description>Zoom in to see more!</description><styleUrl>%s/kml_styles.py#zoom_placemark</styleUrl><Point><coordinates>' % (BASE_URL,)
		kml_output += '%s,%s,0' % (center_lon,center_lat)
		kml_output += '</coordinates></Point></Placemark>'

	# KML footer
	kml_output += '</Folder>\n'
	

	# Print KML output
	return kml_output


# If file called directly, output KML
if __name__ == "__main__":
	# Import cgi module to get query string
	import cgi
	
	try:
		# Get query string
		qv = cgi.FieldStorage()
	except:
		#qv["BBOX"] = "0,0,0,0"
		# Los Angeles
		qv["BBOX"] = "-118.13,33.68,-118.06,33.79"
		qv["GE_KEY"] = ''
	
	
	# Process bounding box to obtain Lat and Long boundaries
	try:
		bbox = qv["BBOX"].value.split(",")
	except:
		#bbox = str("0,0,0,0").split(",")
		# Los Angeles
		bbox = str("-118.13,33.68,-118.06,33.79").split(",")
	
	# Get user name
	try:
		ge_key = qv["GE_KEY"].value
	except:
		ge_key = ''
	
	# Print content-type header
	print GeoUtils.Interface.ContentType("kml")
	print 
	
	print GeoUtils.Interface.StdKML(KMLout(bbox=bbox,ge_key=str(ge_key)))
	
