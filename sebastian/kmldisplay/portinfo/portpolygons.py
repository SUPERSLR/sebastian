#!/usr/bin/python
# David Newell
# kmldisplay/portinfo/portpolygons.py
# Display KML features in Google Earth
# Port Polygons

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Connect to database
DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')


# Generate KML for Port Polygon Legend
def legendKML():
	# Begin legend ScreenOverlay
	kml_output = '<ScreenOverlay>\n'
	
	kml_output += '<name>Port Polygon Legend</name>\n'
	kml_output += '<Icon>\n'
	
	# Legend image location
	kml_output += '<href>%s/kml_images/PortPolygonLegend.png</href>\n' % (BASE_URL,)
	
	kml_output += '</Icon>\n'
	
	# Map a point on the image to a point on the screen
	# Point on image
	kml_output += '<overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n'
	# Point on screen
	kml_output += '<screenXY x="0" y="20" xunits="fraction" yunits="pixels"/>\n'
	
	
	kml_output += '<rotationXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n'
	kml_output += '<size x="0" y="0" xunits="fraction" yunits="fraction"/>\n'
	
	# End legend ScreenOverlay
	kml_output += '</ScreenOverlay>\n'
	
	# Return formatted legend KML 
	return kml_output


# Generate Port Polygon KML
# bbox - bounding box from Google Earth (default: New York City)
# ge_key - user's identification key (default: blank)
# type - type of port polygon (default: Port Infrastructure Polygon)
def KMLout(bbox=["-74.4","40.4","-73.5","40.9"],ge_key="",type="Port Infrastructure Polygon"):
	# Dictionary of IDs associated with type
	polyIDs = {
			"Port Infrastructure Polygon" : 'PortInfraPoly',
			"Basin Polygon" : 'BasinPoly',
			"Model Avoid Polygon" : 'AvoidPoly',
			"Model StartEnd Polygon" : 'StartEndPoly'
		}
	
	# Dictionary of KML Styles associated with type
	polyStyles = {
			"Port Infrastructure Polygon" : 'portInfrastructure',
			"Basin Polygon" : 'basinPolygon',
			"Model Avoid Polygon" : 'avoidPolygon',
			"Model StartEnd Polygon" : 'startEndPolygon'
		}
	
	# Dictionary of heights associated with polygon types
	polyHeights = {
			"Port Infrastructure Polygon" : 120,
			"Basin Polygon" : 20,
			"Model Avoid Polygon" : 50,
			"Model StartEnd Polygon" : 75
		}
	
	
	# Get BBOX boundaries
	west = bbox[0]
	east = bbox[2]
	north = bbox[3]
	south = bbox[1]
	
	# Database query
	dbq = "SELECT ID,portID,AsText(feature_geometry) FROM current_features WHERE feature_type = '%s' AND MBRIntersects(PolyFromText('%s'),feature_geometry)" % (type,GeoUtils.makeBoundingPolygon(north,south,east,west))
	
	# Query database
	dbdata,rowcount = DBhandle.query(dbq)
	
	if rowcount > 0:
		# Folder contents
		import operator
		FolderContents = reduce(operator.concat,[GeoUtils.Interface.genKML.InterfacePortPolygon(ge_key,polyIDs.get(type),polyStyles.get(type),polyHeights.get(type,0),r) for r in dbdata])
	else:
		FolderContents = ''
	
	# Folder details
	FolderID = str(polyIDs.get(type))
	FolderName = '%ss' % (type,)
	FolderStyle = '%s/kml_styles.py#check-hide-children' % (BASE_URL,)
	FolderOpen = 0
	FolderVisibility = 1
	
	# Create output
	kml_output = GeoUtils.Interface.genKML.Folder(id=FolderID,name=FolderName,open=FolderOpen,visibility=FolderVisibility,contents=FolderContents)
	
	# Return KML output
	return kml_output


# If file called directly, output KML
if __name__ == "__main__":
	# Import cgi module to get query string
	# Import operator for concatenation function
	import cgi, operator
	
	try:
		# Get query string
		qv = cgi.FieldStorage()
	except:
		#qv["BBOX"] = "0,0,0,0"
		# New York City
		qv["BBOX"] = "-74.4,40.4,-73.5,40.9"
		qv["GE_KEY"] = ''
	
	
	# Process bounding box to obtain LatLon boundaries
	try:
		bbox = qv["BBOX"].value.split(",")
	except:
		#bbox = str("0,0,0,0").split(",")
		# New York City
		bbox = str("-74.4,40.4,-73.5,40.9").split(",")
	
	# Get user name
	try:
		ge_key = qv["GE_KEY"].value
	except:
		ge_key = ''
	
	PolyTypes = ["Port Infrastructure Polygon","Basin Polygon","Model Avoid Polygon","Model StartEnd Polygon"]
	
	# Print content-type header
	print GeoUtils.Interface.ContentType("kml")
	print 
	
	print GeoUtils.Interface.StdKMLHeader()
	print reduce(operator.concat,[KMLout(bbox=bbox,ge_key=str(ge_key),type=t) for t in PolyTypes])
	print legendKML()
	print GeoUtils.Interface.StdKMLFooter()
	
	# Close database
	DBhandle.close()
	
	
