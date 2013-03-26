#!/usr/bin/python
# Ben Pedrick
# GeoUtils/constants.py
# Constants used throughout the program

class Equations:
        KMB2  = "KMB2"
        BMASW = "BMASW"
        SMCDD = "SMCDD"

class ElevSrc:
        GOOGLE = "google_web_service"
        DEFAULT30SEC = "default_30sec"
        USGS = "usgs_3sec"
        GOOGLE30SEC = "google_web_service_30sec"
        GOOGLE3SEC = "google_web_service_3sec"
        GOOGLEP3SEC = "google_web_service_point3sec"
        NOAAASTER30M = "noaa_aster_30m"

class RegionSrc:
        AFRICA = "africa"
        ASIA = "asia"
        EUROPE = "europe"
        MIDDLEEAST = "middle_east"
        NORTHAMERICA = "north_america"
        OCEANIA = "oceania"
        SOUTHAMERICA = "south_america"

ElevSize = {
        ElevSrc.GOOGLE : 0.0008333333333,
        ElevSrc.DEFAULT30SEC : 0.0083333333333,
        ElevSrc.USGS : 0.0008333333333,
      #  ElevSrc.GOOGLE30SEC : 0.0083333333333,
        ElevSrc.GOOGLE30SEC : 0.001666,
      #  ElevSrc.GOOGLE3SEC  : 0.0008333333333,
        ElevSrc.GOOGLE3SEC  : 0.0083333333333,
      #  ElevSrc.GOOGLEP3SEC : 0.0000833333333,
      #  ElevSrc.GOOGLEP3SEC : 0.00345,
      #  ElevSrc.GOOGLEP3SEC : 0.0083333333333,
        ElevSrc.GOOGLEP3SEC : 0.0008333,
        ElevSrc.NOAAASTER30M : 0.0002777,
    }

ElevRegions = {
        RegionSrc.AFRICA : "africa",
        RegionSrc.ASIA : "asia",
        RegionSrc.EUROPE : "europe",
        RegionSrc.MIDDLEEAST : "middle_east",
        RegionSrc.NORTHAMERICA : "north_america",
        RegionSrc.OCEANIA : "oceania",
        RegionSrc.SOUTHAMERICA : "south_america",
    }

contactEmail = 'info@seaports2100.org'
AmazonExternalHost = 'ec2-184-72-176-76.compute-1.amazonaws.com'
DreamhostHost = 'local.seaports2100.org'
BASE_URL = 'http://%s/sebastian' % (DreamhostHost,)
AmazonDBHost = 'localhost'
DreamhostDBHost = 'localhost'


def computeCenter():
        # Dictionary of compute centers
        computeCenters = {
                        "Amazon Cloud" : ["domU-12-31-39-02-29-81"],
                        "Dreamhost" : ["spiderman"],
                        "Development Server" : ["lappy"],
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

# return the database table holding the lat/lng information for a selected point and data set
def getShardTable(lat, lng, dataset):
        if dataset == ElevSrc.GOOGLE or dataset == ElevSrc.DEFAULT30SEC or dataset == ElevSrc.USGS or dataset == ElevSrc.GOOGLE3SEC or dataset == ElevSrc.GOOGLE30SEC or dataset == ElevSrc.GOOGLEP3SEC or dataset == ElevSrc.NOAAASTER30M :
                shard_name = 'unknown'
                if lng >= -180 and lng < -120 :
                        shard_name = 'shard01'
                elif lng >= -120 and lng < -60 :
                        shard_name = 'shard02'
                elif lng >= -60 and lng < 0 :
                        shard_name = 'shard03'
                elif lng >= 0 and lng < 60 :
                        shard_name = 'shard04'
                elif lng >= 60 and lng < 120 :
                        shard_name = 'shard05'
                elif lng >= 120 and lng <= 180 :
                        shard_name = 'shard06'
                if shard_name == 'unknown' :
                        print "no table was found for the requested point"
                        return 'no data', True
                else :
                        data_table_name = "elev_data_%s_%s" % (shard_name,dataset,)
                        return data_table_name, False

        else :
                print "dataset has not been set up in sharding function"
                return 'dataset invalid', True
# return the database table holding the lat/lng information for a selected point and data set
def getAllShardTables(dataset):
        if dataset == ElevSrc.GOOGLE or dataset == ElevSrc.DEFAULT30SEC or dataset == ElevSrc.USGS or dataset == ElevSrc.GOOGLE3SEC or dataset == ElevSrc.GOOGLE30SEC or dataset == ElevSrc.GOOGLEP3SEC or dataset == ElevSrc.NOAAASTER30M :
                return ["shard01","shard02","shard03","shard04","shard05","shard06" ], False
        else :
                print "dataset has not been set up in sharding function"
                return 'dataset invalid', True
