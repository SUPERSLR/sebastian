#!/usr/bin/python
# David Newell
# sebastian/userfilegen.py
# Generate user-specific KML file for Sebastian GeoData System

BASE_PATH = "/var/www/local.seaports2100.org/"

# Import Useful Modules
import sys
sys.path.append(BASE_PATH)
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Connect to database
DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')



def KMLfileGen(name):
    # KML Body
    kml_output = '<NetworkLink id="kmllib">\n'
    kml_output += '<name>SUPERSLR KML Files</name>\n'
    kml_output += '<visibility>0</visibility>\n'
    kml_output += '<open>1</open>\n'
    kml_output += '<Link>\n'
    kml_output += '<href>%s/kmllib.py</href>\n' % (BASE_URL,)
    kml_output += '<httpQuery>GE_KEY='

    userq = 'SELECT GE_KEY FROM users WHERE name="%s"' % (name,)
    userd,userrc = DBhandle.query(userq)

    if userrc == 0 or userrc > 1:
        raise NameError, 'Invalid Name Entered'

    kml_output += str(userd[0]['GE_KEY'])

    kml_output += '</httpQuery>\n'
    kml_output += '</Link>\n'
    kml_output += '</NetworkLink>\n'


    # Return KML
    return kml_output


# If file called directly, output html
if __name__ == "__main__":
    # Retrieve user information
    qv = []

    # Import cgi module to get query string
    import cgi

    qv = cgi.FieldStorage()

    try:
        name = str(qv["name"].value)
    except KeyError:
        name = 'Guest1'

    name = name.replace("_"," ")

    response = False

    try:
        response = KMLfileGen(name)
    except:
        print GeoUtils.Interface.ContentType("html")
        print

        print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
        import sys,traceback
        print 'Unexpected error:<br/><br/>\n<pre>\n'
        print traceback.format_exc()
        print '\n</pre>\n'
        print GeoUtils.Interface.StdHTMLFooter()

    if response:
        # Print content-type header
        print GeoUtils.Interface.ContentType("kml")
        print
        print GeoUtils.Interface.StdKML(response)

    DBhandle.close()
