#!/usr/bin/python
# David Newell
# GeoUtils/functions.py
# Geographical Utilities package functions


def makeBoundingPolygon(north=90,south=-90,east=180,west=-180):
    """
    Function to create a MySQL bounding rectangular polygon based on four edge points
    
    Inputs:
        north, south, east, west - latitude/longitude values for each boundary of polygon
    Output:
        MySQL Formatted Polygon with single ring:
        POLYGON((points))
    """
    boundingPoly = "POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))" % (west,north,east,north,east,south,west,south,west,north)
    return boundingPoly

