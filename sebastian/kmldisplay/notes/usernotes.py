#!/usr/bin/python
# David Newell
# kmldisplay/notes/usernotes.py
# Display KML features in Google Earth
# User Notes

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Connect to database
DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')


# Generate User Notes KML
# bbox - bounding box from Google Earth (default: New York City)
# ge_key - user's identification key (default: blank)
def KMLout(bbox=["-74.4","40.4","-73.5","40.9"],ge_key=""):
    # Dictionary of KML Styles associated with type
    noteStatusStyle = {
            "Caution" : 'noteCaution',
            "Sticky" : 'noteSticky',
            "Info" : 'noteInfo',
            "Hidden" : 'noteHidden'
        }
    
    
    # Get BBOX boundaries
    west = bbox[0]
    east = bbox[2]
    north = bbox[3]
    south = bbox[1]
    
    # Database query
    dbq = "SELECT ID,attribution,details,status,visible,AsText(feature_geometry) FROM notes WHERE MBRIntersects(PolyFromText('%s'),feature_geometry) AND visible=1" \
        % (GeoUtils.makeBoundingPolygon(north,south,east,west),)
    
    # Query database
    dbdata,rowcount = DBhandle.query(dbq)
            
    # Close database
    DBhandle.close()
    
    if rowcount > 0:
        # Folder contents
        import operator
        FolderContents = reduce(operator.concat,[GeoUtils.Interface.genKML.InterfaceNotePlacemark(ge_key,noteStatusStyle,r) for r in dbdata])
    else:
        FolderContents = ''
    
    # Folder details
    FolderID = 'UserNotes'
    FolderName = 'User Notes'
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
    print GeoUtils.Interface.ContentType("kml")
    print 
    
    print GeoUtils.Interface.StdKML(KMLout(bbox=bbox,ge_key=str(ge_key)))
    
    
