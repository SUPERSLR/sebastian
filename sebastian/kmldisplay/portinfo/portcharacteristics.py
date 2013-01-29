#!/usr/bin/python
# David Newell
# kmldisplay/portinfo/portcharacteristics.py
# Display KML features in Google Earth
# Port Characteristics

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Connect to database
DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')


# Generate KML
# ge_key - user's identification key (default: blank)
def KMLout(ge_key=""):
	# Database query
	dbq = "SELECT ID,name,latitude,longitude,analysis_complete FROM portdata"
	
	# Query database
	dbdata,rowcount = DBhandle.query(dbq)
	
	# Style dictionary
	PortStyles = {
				0 : '%s/kml_styles.py#portCharacteristicsIncomplete' % (BASE_URL,),
				1 : '%s/kml_styles.py#portCharacteristicsPartComplete' % (BASE_URL,),
				2 : '%s/kml_styles.py#portCharacteristicsComplete' % (BASE_URL,)
		}
	
	if rowcount > 0:
		# Folder contents
		import operator
		FolderContents = reduce(operator.concat,[GeoUtils.Interface.genKML.InterfacePortCharPlacemark(ge_key,PortStyles,r) for r in dbdata])
	else:
		FolderContents = ''
	
	# Folder details
	FolderID = 'PortCharacteristics'
	FolderName = 'Port Characteristics'
	FolderStyle = '%s/kml_styles.py#check-hide-children' % (BASE_URL,)
	FolderOpen = 0
	FolderVisibility = 1
	
	# Create output
	kml_output = GeoUtils.Interface.genKML.Folder(id=FolderID,name=FolderName,open=FolderOpen,visibility=FolderVisibility,contents=FolderContents)
	
	# Print KML output
	return kml_output


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
	
	# Close database
	DBhandle.close()
