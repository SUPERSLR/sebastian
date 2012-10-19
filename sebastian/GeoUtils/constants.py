#!/usr/bin/python
# Ben Pedrick
# GeoUtils/constants.py
# Constants used throughout the program

class Equations:
	BMASW = "BMASW"
	SMCDD = "SMCDD"

class ElevSrc:
	GOOGLE = "google_web_service"
	DEFAULT30SEC = "default_30sec"
	USGS = "usgs_3sec"

ElevSize = {
        ElevSrc.GOOGLE : 0.0008333333333,
        ElevSrc.DEFAULT30SEC : 0.0083333333333,
        ElevSrc.USGS : 0.0008333333333,
    }


contactEmail = 'info@seaports2100.org'
AmazonExternalHost = 'ec2-184-72-176-76.compute-1.amazonaws.com'
DreamhostHost = 'sebastian.seaports2100.org'
BASE_URL = 'http://%s/sebastian' % (DreamhostHost,)
AmazonDBHost = 'localhost'
DreamhostDBHost = 'mysql.seaports2100.org'


def computeCenter():
	# Dictionary of compute centers
	computeCenters = {
			"Amazon Cloud" : ["domU-12-31-39-02-29-81"],
			"Dreamhost" : ["spiderman"],
			"Unavailable" : ["unavailable"]
		}
	
	# Try to get computer name
	try:
		import socket
		computerName = socket.gethostname()
	except:
		computerName = "unavailable"
	
	computeCenter = "Unavailable"
	
	for center in computeCenters:
		if computerName in computeCenters[center]:
			computeCenter = center
			break
	
	return computeCenter

