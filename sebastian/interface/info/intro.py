#!/usr/bin/python
# Ben Pedrick
# intro.py
# Launching point for getting Sebastian information

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


if __name__ == "__main__":
	# Print headers
	print GeoUtils.Interface.ContentType("html")
	print

	print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
	print '<h2>Information Home</h2>'
	print '<p>Here you can find all sorts of information collected in Sebastian.</p>'
	print '<h3>Choose a subject</h3>'
	print GeoUtils.Interface.buildButton('Information by Region', 'lens', '/sebastian/interface/info/regions.py', {})
	print GeoUtils.Interface.buildButton('Comparisons', 'lens', '/sebastian/interface/info/compare.py', {})
	print GeoUtils.Interface.buildButton('Completion Status', 'lens', '/sebastian/interface/info/status.py', {})
	print GeoUtils.Interface.StdHMTLFooter()
