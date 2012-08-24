#!/usr/bin/python
# Ben Pedrick
# status.py
# Gives some system wide updates of how things are going.

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


def getInfo():
	''' Gets information to display, and returns HTML formatted string of data '''

	# keep queries together for easy finding
	queries = {
			"ports" : 'SELECT * from portdata',
			"paths" : 'SELECT * from portprotector',
		}

	# Connect to database
	DBhandle = GeoUtils.RDB()
	DBhandle.connect('uws_ge')

	# -------------------------------------------
	#
	# Port Info
	#
	# -------------------------------------------
	portData, portCount = DBhandle.query(queries['ports'])

	output = "<h2>Completion Status</h2>\n<h3>Ports</h3><p>\n<strong>Total Number of Ports: </strong>" + str(portCount) +\
			"\n"

	portStatus = (len([row for row in portData if row['analysis_complete'] == 0]),\
		len([row for row in portData if row['analysis_complete'] == 1]),
		len([row for row in portData if row['analysis_complete'] == 2]))

	output += "<ul><li>Complete: " + str(portStatus[2]) + "</li>"\
		"<li>Partially Complete: " + str(portStatus[1]) + "</li>"\
		"<li>Incomplete: " + str(portStatus[0]) + "</li></ul>"

	output += "</p>"


	# -------------------------------------------
	#
	# Path Info
	#
	# -------------------------------------------
	pathData, pathCount = DBhandle.query(queries['paths'])

	output += "<h3>Protector Path</h3>"

	# Get path data
	ucsdPaths = [row for row in pathData if row['elev_data'] == 'default_30sec']
	usgsPaths = [row for row in pathData if row['elev_data'] == 'usgs_3sec']
	googlePaths = [row for row in pathData if row['elev_data'] == 'google_web_service']


	# Output number of paths, total length, and total volume of each
	output += "<p>There are <strong>" + str(len(ucsdPaths)) +\
		"</strong> paths using the 30 second UCSD grid.\n"
	output += "<ul>\n<li>Total Length: " + str(sum([obj['path_length'] for obj in ucsdPaths])) +\
		" meters.</li>\n"
	output += "<li>Total Volume: " + str(sum([obj['path_volume'] for obj in ucsdPaths])) +\
		" cubic meters.</li>\n"
	output += "</ul></p>\n"

	output += "<p>There are <strong>" + str(len(usgsPaths)) +\
		"</strong> paths using the 3 second USGS grid.\n"
	output += "<ul><li>Total Length: " + str(sum([obj['path_length'] for obj in usgsPaths])) +\
		" meters.</li>\n"
	output += "<li>Total Volume: " + str(sum([obj['path_volume'] for obj in usgsPaths])) +\
		" cubic meters.</li></ul>\n"
	output += "</ul></p>\n"
	
	output += "<p>There are <strong>" + str(len(googlePaths)) +\
		"</strong> paths using the Google Elevation data.\n"
	output += "<ul><li>Total Length: " + str(sum([obj['path_length'] for obj in googlePaths])) +\
		" meters.</li>\n"
	output += "<li>Total Volume: " + str(sum([obj['path_volume'] for obj in googlePaths])) +\
		" cubic meters.</li></ul>\n"
	output += "</ul></p>\n"

	output += GeoUtils.Interface.buildButton('Country Information', 'lens', '/sebastian/interface/info/countries.py', {})
	output += GeoUtils.Interface.buildButton('Information Home', 'lens', '/sebastian/interface/info/intro.py', {})

	DBhandle.close()

	return output


# if called directly, output html
if __name__ == "__main__":

	print GeoUtils.Interface.ContentType("html")
	print
    
	print GeoUtils.Interface.StdHTML(GeoUtils.Interface.uniForm.HTMLHeaderInfo(),getInfo())
