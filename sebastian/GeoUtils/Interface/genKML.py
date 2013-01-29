#!/usr/bin/python
# David Newell
# GeoUtils/Interface/genKML.py
# Geographical Utilities Interface package
# Generate KML functions

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
from GeoUtils.constants import BASE_URL
from GeoUtils import Features


def Placemark(id,name,coordinates,style="",description=""):
    '''
    Generate Placemark
    
      id          - Placemark ID
      name        - Placemark Name
      coordinates - Placemark coordinates as KML
      style       - Placemark styleURL
      description - Placemark description
    '''
    
    kml = '<Placemark id="%s"><name>%s</name>\n' % (id,name)
    kml += '<styleUrl>%s</styleUrl>\n' % (style,)
    kml += '<description>\n%s</description>\n' % (description,)
    kml += str(coordinates)
    kml += '</Placemark>\n'
    
    return kml


def Folder(id,name,open=0,visibility=0,style="",contents=""):
    '''
    Generate Folder
    
      id         - Folder ID
      name       - Folder Name
      open       - Folder default open/closed
      visibility - Folder default visibility
      style      - Folder styleURL
      contents   - KML inside folder
    '''
    
    kml = '<Folder id="%s">\n' % (id,)
    kml += '<styleUrl>%s</styleUrl>\n' % (style,)
    kml += '<name>%s</name><open>%s</open><visibility>%s</visibility>\n' % (name, open, visibility)
    kml += str(contents)
    kml += '</Folder>\n'
    
    return kml


def ScreenOverlay(id,name,iconHREF,overlayXY,screenXY,rotationXY,size):
    # Begin legend ScreenOverlay
    kml = '<ScreenOverlay>\n'
    
    kml += '<name>Port Polygon Legend</name>\n'
    kml += '<Icon>\n'
    
    # Legend image location
    kml += '<href>%s/kml_images/PortPolygonLegend.png</href>\n' % (BASE_URL,)
    
    kml += '</Icon>\n'
    
    # Map a point on the image to a point on the screen
    # Point on image
    kml += '<overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n'
    # Point on screen
    kml += '<screenXY x="0" y="20" xunits="fraction" yunits="pixels"/>\n'
    
    
    kml += '<rotationXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n'
    kml += '<size x="0" y="0" xunits="fraction" yunits="fraction"/>\n'
    
    # End legend ScreenOverlay
    kml += '</ScreenOverlay>\n'
    
    return kml



def InterfacePath(ge_key,PathInfo):
    # Add GE_KEY to simplify string processing below
    PathInfo["GE_KEY"] = ge_key
    
    # ID, Name, and Style
    PlacemarkID = 'ModelPath-%(ID)s' % PathInfo
    PlacemarkName = '%(portID)s' % PathInfo
    PlacemarkStyle = '%s/kml_styles.py#modelPath' % (BASE_URL)
    
    # iframe located in description
    PlacemarkDescription = '<iframe src="%s/interface/main.py?item=ModelPath' % (BASE_URL,)
    PlacemarkDescription += '-%(ID)s&amp;GE_KEY=%(GE_KEY)s&amp;portID=%(portID)s" width="400" height="500"></iframe>' % PathInfo
    
    # Convert MySQL geometry to KML (polygon)
    Geometry = Features.Path()
    Geometry.fromMySQL_linestring(PathInfo["AsText(path_geometry)"])
    PlacemarkCoords = Geometry.toKML(height=250,altmode="relativeToSeaFloor",extrude="yes")
    
    return Placemark(id=PlacemarkID,name=PlacemarkName,coordinates=PlacemarkCoords,style=PlacemarkStyle,description=PlacemarkDescription)


def InterfaceNotePlacemark(ge_key,noteStatusStyle,NoteInfo):
    # Add GE_KEY to r to simplify string formatting
    NoteInfo["GE_KEY"] = ge_key
    
    # ID, Name, and Style
    PlacemarkID = 'UserNote-%(ID)s' % NoteInfo
    PlacemarkName = 'Note %(ID)s (%(attribution)s)' % NoteInfo
    
    if NoteInfo["visible"] == 0 or NoteInfo["visible"] == '0':
        PlacemarkStyle = '%s/kml_styles.py#%s' % (BASE_URL,noteStatusStyle.get('Hidden'))
    else:
        PlacemarkStyle = '%s/kml_styles.py#%s' % (BASE_URL,noteStatusStyle.get(NoteInfo["status"]))
    
    # iframe located in description
    PlacemarkDescription = '<iframe src="%s/interface/main.py?item=UserNote' % (BASE_URL,)
    PlacemarkDescription += '-%(ID)s&amp;GE_KEY=%(GE_KEY)s' % NoteInfo
    PlacemarkDescription += '" width="400" height="500"></iframe>'
    
    # Convert MySQL geometry to KML (polygon)
    NotePoint = Features.Point()
    NotePoint.fromMySQL_point(NoteInfo["AsText(feature_geometry)"])
    PlacemarkCoords = NotePoint.toKML(height=0,altmode="clampToGround")
    
    return Placemark(id=PlacemarkID,name=PlacemarkName,coordinates=PlacemarkCoords,style=PlacemarkStyle,description=PlacemarkDescription)


def InterfacePortPolygon(ge_key,polyID,polyStyle,polyHeight,PolygonInfo):
    # Add GE_KEY,PolyStyle, and PolyID to info to simplify string formatting
    PolygonInfo["GE_KEY"] = ge_key
    PolygonInfo["PolyStyle"] = polyStyle
    PolygonInfo["PolyID"] = polyID
    
    # ID, Name, and Style
    PlacemarkID = '%(PolyID)s-%(ID)s' % PolygonInfo
    PlacemarkName = '%(portID)s-%(ID)s' % PolygonInfo
    PlacemarkStyle = '%s/kml_styles.py#%s' % (BASE_URL,polyStyle)
    
    # iframe located in description
    PlacemarkDescription = '<iframe src="%s/interface/main.py?item=%s' % (BASE_URL,polyID)
    PlacemarkDescription += '-%(ID)s&amp;GE_KEY=%(GE_KEY)s&amp;portID=%(portID)s' % PolygonInfo
    PlacemarkDescription += '" width="400" height="500"></iframe>'
    
    # Convert MySQL geometry to KML (polygon)
    poly = Features.Polygon()
    poly.fromMySQL_polygon(PolygonInfo["AsText(feature_geometry)"])
    PlacemarkCoords = poly.toKML(height=polyHeight,altmode="relativeToGround",extrude="yes")
    
    return Placemark(id=PlacemarkID,name=PlacemarkName,coordinates=PlacemarkCoords,style=PlacemarkStyle,description=PlacemarkDescription)


def InterfacePortCharPlacemark(ge_key,PortStyles,PortCharInfo):
    # Add GE_KEY to r to simplify string formatting
    PortCharInfo["GE_KEY"] = ge_key
    
    # ID, Name, and Style
    PlacemarkID = 'PortChar-%(ID)s' % PortCharInfo
    PlacemarkName = '%(name)s (%(ID)s)' % PortCharInfo
    PlacemarkStyle = PortStyles.get(int(PortCharInfo["analysis_complete"]))
    
    # iframe located in description
    PlacemarkDescription = '<iframe src="%s/interface/main.py?item=PortChar' % (BASE_URL,)
    PlacemarkDescription += '-%(ID)s&amp;GE_KEY=%(GE_KEY)s' % PortCharInfo
    PlacemarkDescription += '" width="400" height="500"></iframe>'
    
    # Assemble placemark coordinates
    PlacemarkCoords = '<Point><coordinates>%(longitude)s,%(latitude)s,0</coordinates></Point>\n' % PortCharInfo
    PlacemarkCoords += '<LookAt><longitude>%(longitude)s</longitude><latitude>%(latitude)s</latitude><range>30000</range></LookAt>\n' % PortCharInfo
    
    return Placemark(id=PlacemarkID,name=PlacemarkName,coordinates=PlacemarkCoords,style=PlacemarkStyle,description=PlacemarkDescription)
