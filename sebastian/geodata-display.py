#!/usr/bin/python
# David Newell
# geodata-display.py
# KML display options in Google Earth

BASE_PATH = "/home/jack_sparrow/sebastian.sp/sebastian/"

# Import Useful Modules
import sys
sys.path.append(BASE_PATH)
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Generate KML for display in Google Earth
def buildKML(ge_key=""):

        # Get bounding box limits
        #west = float(bbox[0])
        #east = float(bbox[2])
        #north = float(bbox[3])
        #south = float(bbox[1])

        # Calculate the height and width of view
        #height = north - south
        #width = east - west

        # Find the center point of view
        #center_lon = width / 2 + west
        #center_lat = height / 2 + south


        # KML Header
        kml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        kml += '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        kml += '<Document>\n'

        # Begin Sebastian ScreenOverlay
        kml += '<ScreenOverlay>\n'
        kml += '<name>Sebastian</name>\n'
        kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>\n' % (BASE_URL,)
        kml += '<Icon>\n'
        # Legend image location
        kml += '<href>%s/kml_images/Sebastian.jpg</href>\n' % (BASE_URL,)
        kml += '</Icon>\n'
        # Map a point on the image to a point on the screen
        # Point on image
        kml += '<overlayXY x="0" y="1" xunits="fraction" yunits="fraction"/>\n'
        # Point on screen
        kml += '<screenXY x="0" y="1" xunits="fraction" yunits="fraction"/>\n'
        kml += '<rotationXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n'
        kml += '<size x="100" y="0" xunits="pixels" yunits="fraction"/>\n'
        kml += '<description><![CDATA[<iframe src="%s/interface/main.py?item=Info-0' % (BASE_URL,)
        kml += '&amp;GE_KEY=%s" width="400" height="500"></iframe>]]></description>\n' % (ge_key,)
        # End Sebastian ScreenOverlay
        kml += '</ScreenOverlay>\n'

        # Folder for Port Information
        kml += '<Folder id="portinfo">\n'
        kml += '<name>Port Information</name>\n'
        kml += '<visibility>0</visibility>\n'
        kml += '<open>0</open>\n'

        # Fetch Port Characteristics
        kml += '<NetworkLink id="portCharacteristicsLink">\n'
        kml += '<name>Port Characteristics</name>\n'
        kml += '<visibility>1</visibility>\n'
        kml += '<open>0</open>\n'
        kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
        kml += '<description>Compute Center:<br/>\n<span style="color:green"><strong>%s</strong></span><br /></description>\n' % (GeoUtils.constants.computeCenter(),)
        kml += '<Link>\n'
        kml += '<href>%s/kmldisplay/portinfo/portcharacteristics.py</href>\n' % (BASE_URL,)
        kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
        kml += '</Link>\n'
        kml += '</NetworkLink>\n'

        # Fetch Port Infrastructure Polygons
        kml += '<NetworkLink id="portPolygonsLink">\n'
        kml += '<name>Port Polygons</name>\n'
        kml += '<visibility>1</visibility>\n'
        kml += '<open>0</open>\n'
        kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
        kml += '<description>Compute Center:<br/>\n<span style="color:green"><strong>%s</strong></span><br /></description>\n' % (GeoUtils.constants.computeCenter(),)
        kml += '<Link>\n'
        kml += '<href>%s/kmldisplay/portinfo/portpolygons.py</href>\n' % (BASE_URL,)
        kml += '<refreshInterval>2</refreshInterval>\n'
        kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
        kml += '<viewRefreshTime>3</viewRefreshTime>\n'
        kml += '<viewBoundScale>1.5</viewBoundScale>\n'
        kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
        kml += '</Link>\n'
        kml += '</NetworkLink>\n'

        # Fetch Port Protector Model Paths
        kml += '<NetworkLink id="portProtectorModelPathsLink">\n'
        kml += '<name>Port Protector Model Paths</name>\n'
        kml += '<visibility>1</visibility>\n'
        kml += '<open>0</open>\n'
        kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
        kml += '<description>Compute Center:<br/>\n<span style="color:green"><strong>%s</strong></span><br /></description>\n' % (GeoUtils.constants.computeCenter(),)
        kml += '<Link>\n'
        kml += '<href>%s/kmldisplay/model/paths.py</href>\n' % (BASE_URL,)
        kml += '<refreshInterval>2</refreshInterval>\n'
        kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
        kml += '<viewRefreshTime>3</viewRefreshTime>\n'
        kml += '<viewBoundScale>1.2</viewBoundScale>\n'
        kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
        kml += '</Link>\n'
        kml += '</NetworkLink>\n'

        # Fetch Berm Model Paths
        kml += '<NetworkLink id="bermModelPathsLink">\n'
        kml += '<name>Berm Model Paths</name>\n'
        kml += '<visibility>1</visibility>\n'
        kml += '<open>0</open>\n'
        kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
        kml += '<description>Compute Center:<br/>\n<span style="color:green"><strong>%s</strong></span><br /></description>\n' % (GeoUtils.constants.computeCenter(),)
        kml += '<Link>\n'
        kml += '<href>%s/kmldisplay/model/berm_paths.py</href>\n' % (BASE_URL,)
        kml += '<refreshInterval>2</refreshInterval>\n'
        kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
        kml += '<viewRefreshTime>3</viewRefreshTime>\n'
        kml += '<viewBoundScale>1.2</viewBoundScale>\n'
        kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
        kml += '</Link>\n'
        kml += '</NetworkLink>\n'

        # Close Folder
        kml += '</Folder>\n'

        # Folder for Topography & Bathymetry
        kml += '<Folder id="topographybathymetry">\n'
        kml += '<name>Topography/Bathymetry</name>\n'
        kml += '<visibility>0</visibility>\n'
        kml += '<open>0</open>\n'

        # Fetch Numerical Bathymetry
        kml += '<NetworkLink id="globalCoastalNumericalTopoBathyLink">\n'
        kml += '<name>Global Coastal Numerical Topography-Bathymetry</name>\n'
        kml += '<visibility>0</visibility>\n'
        kml += '<open>0</open>\n'
        kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
        kml += '<description>Current Computation Center:<br/>\n<span style="color:green"><strong>%s</strong></span><br /></description>\n' % (GeoUtils.constants.computeCenter(),)
        kml += '<Link>\n'
        kml += '<href>%s/kmldisplay/topobathy/numerical.py</href>\n' % (BASE_URL,)
#       kml += '<refreshInterval>2</refreshInterval>\n'
#       kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
#       kml += '<viewRefreshTime>3</viewRefreshTime>\n'
#       kml += '<viewBoundScale>1.2</viewBoundScale>\n'
        kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
        kml += '</Link>\n'
        kml += '</NetworkLink>\n'

        # Close Folder
        kml += '</Folder>\n'

        # Folder for Notes
        kml += '<Folder id="notes">\n'
        kml += '<name>Notes</name>\n'
        kml += '<visibility>0</visibility>\n'
        kml += '<open>0</open>\n'

        # Fetch User Notes
        kml += '<NetworkLink id="userNotesLink">\n'
        kml += '<name>User Notes</name>\n'
        kml += '<visibility>0</visibility>\n'
        kml += '<open>0</open>\n'
        kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
        kml += '<description>Compute Center:<br/>\n<span style="color:green"><strong>%s</strong></span><br /></description>\n' % (GeoUtils.constants.computeCenter(),)
        kml += '<Link>\n'
        kml += '<href>%s/kmldisplay/notes/usernotes.py</href>\n' % (BASE_URL,)
        kml += '<refreshInterval>2</refreshInterval>\n'
        kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
        kml += '<viewRefreshTime>3</viewRefreshTime>\n'
        kml += '<viewBoundScale>1.2</viewBoundScale>\n'
        kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
        kml += '</Link>\n'
        kml += '</NetworkLink>\n'

        # Close Folder
        kml += '</Folder>\n'


        # -------------------------------------------
        # Folder for Real-Time views
        kml += '<Folder id="RTview">\n'
        kml += '<name>Real-Time Connected User Views</name>\n'
        kml += '<visibility>1</visibility>\n'
        kml += '<open>0</open>\n'

        # Fetch User Views
        kml += '<NetworkLink id="RTviewLink">\n'
        kml += '<name>Real-Time Connected User Views</name>\n'
        kml += '<visibility>1</visibility>\n'
        kml += '<open>1</open>\n'
        kml += '<styleUrl>%s/kml_styles.py#infoNoIcon</styleUrl>' % (BASE_URL,)
        kml += '<description>Current Status:<br/>\n<span style="color:red"><strong>EXPERIMENTAL</strong></span><br /><em>Runs on Development System</em></description>\n'
        kml += '<Link>\n'
        kml += '<href>%s/RTcollab/GEview.py</href>\n' % (BASE_URL,)
        kml += '<refreshMode>onInterval</refreshMode>'
        kml += '<refreshInterval>30</refreshInterval>\n'
        kml += '<viewRefreshMode>onStop</viewRefreshMode>\n'
        kml += '<viewRefreshTime>3</viewRefreshTime>\n'
        kml += '<viewBoundScale>1</viewBoundScale>\n'
        kml += '<httpQuery>GE_KEY=%s</httpQuery>' % (ge_key,)
        kml += '</Link>\n'
        kml += '</NetworkLink>\n'

        # Close Folder
        kml += '</Folder>\n'
        # -------------------------------------------


        # KML Footer
        kml += '</Document>\n'
        kml += '</kml>\n'

        return kml


# If file called directly, output KML
if __name__ == "__main__":
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

        # Print content-type header
        #print 'Content-type: application/vnd.google-earth.kml+xml'
        print GeoUtils.Interface.ContentType("kml")

        # Alternate MIME-type for debugging
        #print "Content-type: text/html"

        print

        print buildKML(ge_key=str(ge_key))
