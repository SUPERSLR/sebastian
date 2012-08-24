#!/usr/bin/python
# David Newell
# RTcollab/GEview.py
# Capture and display connected users' view information

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')


def createViewPoly(user,data):
    # Create view polygons
    kml = '<Placemark id="ViewInfo-%s"><name>%s</name>\n' % (user,user)
    kml += '<styleUrl>%s/kml_styles.py#connUserViewPolygon' % (BASE_URL,)
    kml += '</styleUrl>\n'
    kml += '<description>\n'
    kml += '<p>Last time connected: %s</p>\n' % (data['timestamp'].strftime("%A, %B %d, %Y  -  %I:%M%p"),)
    kml += '</description>\n'
    
    viewpoly = GeoUtils.Features.Polygon()
    viewpoly.fromMySQL_polygon(data['view'])
    kml += viewpoly.toKML(height=100,altmode="relativeToGround",extrude="yes")
    
    #kml += GeoMySQL.poly2kml(input=data['view'],height=100,altmode="relativeToGround",extrude="yes")
    
    kml += '</Placemark>\n'
    
    return kml



def processGEview(bbox,ge_key):
    # Get current user's information
    DBhandle.setUser(ge_key)
    user = DBhandle.ConnUserName()
    
    # Import shelving and datetime modules
    import shelve
    from datetime import datetime, timedelta
    
    # Get BBOX boundaries
    west = float(bbox[0])
    east = float(bbox[2])
    north = float(bbox[3])
    south = float(bbox[1])
    
    # If large view, create small square view at center
    if abs(east-west) > 30 or abs(north-south) > 30:
        center_lng = ((east - west) / 2) + west
        center_lat = ((north - south) / 2) + south
        west = center_lng - 0.2
        east = center_lng + 0.2
        north = center_lat + 0.2
        south = center_lat - 0.2
    
    # Create bounding polygon
    boundingPoly = GeoUtils.makeBoundingPolygon(north,south,east,west)
    
    # KML Header
    kml_output = '<Folder id="ConnUserViewInfo">\n'
    kml_output += '<styleUrl>%s/kml_styles.py#check-hide-children</styleUrl>\n' % (BASE_URL,)
    kml_output += '<name>Connected User View Information</name><open>0</open><visibility>1</visibility>\n'
    
    # Open persistent object storage
    s = shelve.open('realtimeGEuserview.db', writeback=True)
    
    try:
        if not 'liveview' in s:
            s.update(liveview={})
        
        s['liveview'][user] = { 'timestamp' : datetime.now(), 'view' : boundingPoly }
        
        for u in s['liveview'].keys():
            if s['liveview'][u]['timestamp'] + timedelta(minutes = 5) < datetime.now():
                del s['liveview'][u]
            elif u == "visitor":
                continue
            else:
                if not s['liveview'][u]['view'] == boundingPoly:
                    kml_output += createViewPoly(u, s['liveview'][u])
        
    finally:
        s.close()
    
    
    # KML footer
    kml_output += '</Folder>\n'
    
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
    
    # Print content-type header
    print GeoUtils.Interface.ContentType('kml')
    
    # Alternate MIME-type for debugging
    #print GeoUtils.Interface.ContentType('html')
    
    # Print blank line
    print 
    
    # Print KML
    print GeoUtils.Interface.StdKML(processGEview(bbox=bbox,ge_key=str(ge_key)))
