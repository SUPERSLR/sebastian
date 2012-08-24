#!/usr/bin/python
# David Newell
# GeoUtils/Features.py
# Geographical Features module


class Point:
    '''
    Class for storing point features
    
        Storage Variables:
            lon - point longitude
            lat - point latitude
            elev - point elevation
        
        Methods:
            __init__(x,y,elev)
            isLonSet()
            isLatSet()
            isElevSet()
            setLon(x)
            setLat(y)
            setElev(elev)
            fromKML(kml)
            toMySQL_point()
            toKML(height,altmode)
            toDict()
            toKMLcoords()
            toMySQLcoords()
            distanceFrom(point)
    
    '''
    def __init__(self,x=None,y=None,elev=None):
        self.lon = x
        self.lat = y
        self.elev = elev
    
    
    def isLonSet(self):
        return self.lon != None
    
    
    def isLatSet(self):
        return self.lat != None
    
    
    def isElevSet(self):
        return self.elev != None
    
    
    def setLon(self,x):
        self.lon = float(x)
    
    
    def setLat(self,y):
        self.lat = float(y)
    
    
    def setElev(self,elev):
        self.elev = float(elev)
    
    
    def fromMySQL_point(self,mysql):
        # Strip LINESTRING from MySQL format LINESTRING(points)
        m = str(mysql).replace('POINT(','').replace(')','')
        
        # Split into longitude and latitude
        coord = m.split(' ')
        
        # Set coordinates based on input
        self.lon = float(coord[0])
        self.lat = float(coord[1])
    
    
    def fromKML(self,kml):
    	# Import XML Parser
    	from xml.dom.minidom import parseString
    	
    	# Parse KML
    	k = parseString(kml)
    	
    	# Retrieve coordinates
    	coord = k.getElementsByTagName("coordinates")[0].firstChild.data.strip().split(",")
    	
    	# Set coordinates based on input
    	self.lon = float(coord[0])
    	self.lat = float(coord[1])
    	self.elev = float(coord[2])
    
    
    def toMySQL_point(self):
        # Begin MySQL Point output
        output = 'POINT('
        
        # Get coordinates
        output += self.toMySQLcoords()
        
        # End point output
        output += ")"
        
        # Return formatted MySQL Point
        return output
    
    
    def toKML(self,height=0,altmode="clampToGround"):
        # Begin LineString output
        output = "<Point>\n"
        
        # Import KML Options Dictionaries
        import KMLOptions
        
        # Get altitude mode
        output += KMLOptions.altitudeMode.get(altmode)
        
        # Begin coordinate output
        output += "<coordinates>"
        
        # Process coordinates
        output += self.toKMLcoords() + " "
        
        # End coordinate output
        output += "</coordinates>\n"
        
        # End LineString output
        output += "</Point>\n"
        
        # Return formatted KML LineString
        return output
    
    
    def toDict(self):
        return { "lon" : self.lon , "lat" : self.lat, "elev" : self.elev }
    
    
    def toKMLcoords(self):
        if self.elev == None:
            return str(self.lon) + "," + str(self.lat) + ",0"
        else:
            return str(self.lon) + "," + str(self.lat) + "," + str(self.elev)
    
    
    def toMySQLcoords(self):
        return str(self.lon) + " " + str(self.lat)
    
    
    def distanceFrom(self,point):
        """
        Calculate distance (in meters) between two points given as (lon,lat) pairs
        based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
        Implementation inspired by JavaScript implementation from 
        http://www.movable-type.co.uk/scripts/latlong.html
        """
        
        import math
        
        # Average Radius of earth in meters
        earthRadius = float(6371) * float(1000)
        
        # Convert latitude and longitude to radians
        start_lon = math.radians(float(self.lon))
        start_lat = math.radians(float(self.lat))
        end_lon = math.radians(float(point.lon))
        end_lat = math.radians(float(point.lat))
        
        # Calculate difference in latitude and longitude
        latDiff = end_lat - start_lat
        lonDiff = end_lon - start_lon
        
        # Find total length
        a_t = math.sin(latDiff/2)**2 + math.cos(start_lat) * math.cos(end_lat) * math.sin(lonDiff/2)**2
        c_t = 2 * math.atan2(math.sqrt(a_t),math.sqrt(1-a_t))
        totalLength = earthRadius * c_t
        
        # Find horizontal length
        a_x = math.cos(start_lat) * math.cos(end_lat) * math.sin(lonDiff/2)**2
        c_x = 2 * math.atan2(math.sqrt(a_x),math.sqrt(1-a_x))
        xLength = earthRadius * c_x
        
        # Find vertical length
        a_y = math.sin(latDiff/2)**2
        c_y = 2 * math.atan2(math.sqrt(a_y),math.sqrt(1-a_y))
        yLength = earthRadius * c_y
        
        # Return dictionary of lengths 
        return { "total" : totalLength , "horiz" : xLength , "vertical" : yLength }



# Class for storing polygons
#   outercoords - list of Points on outer boundary
#   innercoords - list of lists of Points describing inner boundaries
#   irings - number of inner rings
class Polygon:
    '''
    Class for storing polygon features
    '''
    def __init__(self):
        self.outercoords = []
        self.innercoords = []
        self.irings = None
    
    
    def outerpts(self):
        return len(self.outercoords)
    
    
    def innerrings(self):
        return self.irings
    
    
    def fromMySQL_polygon(self,mysql):
        # Strip POLYGON from MySQL format POLYGON((points),(points),(points)) and split into polyline coordinates
        i = str(mysql).replace('POLYGON((','').replace('))','').split('),(')
        
        # Calculate number of rings
        rings = len(i)
        
        # If rings is one, set irings to 0 otherwise number of inner rings
        if rings == 1:
            self.irings = None
        else:
            self.irings = rings - 1
        
        # Get outer ring coordinates
        self.outercoords = []
        oc = i[0].split(",")
        for pt in oc:
            lon,lat = pt.split(" ")
            self.outercoords.append(Point(lon,lat))
        
        # For each ring
        self.innercoords = []
        for n in range(1,rings):
            ring = []
            ic = i[n].split(",")
            for pt in ic:
                lon,lat = pt.split(" ")
                ring.append(Point(lon,lat))
            self.innercoords.append(ring)
    
    
    def fromKML(self,kml):
        # Import XML parser
        from xml.dom.minidom import parseString
        
        # Parse KML input
        parsedKML = parseString(kml)
        
        # Get outer rings coordinates
        self.outercoords = []
        oc = parsedKML.getElementsByTagName("outerBoundaryIs")[0].getElementsByTagName("coordinates")[0].firstChild.nodeValue.strip().split(" ")
        for coord in oc:
            lon,lat,elev = coord.split(",")
            self.outercoords.append(Point(lon,lat,elev))
        
        # Get number of inner rings
        self.irings = len(parsedKML.getElementsByTagName("innerBoundaryIs"))
        
        if self.irings == 0:
            self.irings = None
        else:
            # Initialize inner rings coordinates
            self.innercoords = []
            
            # For each inner ring, add to output
            for n in range(self.irings):
                # Get ring coordinates
                ring = []
                ic = parsedKML.getElementsByTagName("innerBoundaryIs")[n].getElementsByTagName("coordinates")[0].firstChild.nodeValue.strip().split(" ")
                for coord in ic:
                    lon,lat,elev = coord.split(",")
                    ring.append(Point(lon,lat,elev))
                self.innercoords.append(ring)
    
    
    def fromPointList(self,outer,inner=[]):
        for pt in outer:
            if len(pt) == 3:
                self.outercoords.append(Point(pt[0],pt[1],pt[2]))
            elif len(pt) == 2:
                self.outercoords.append(Point(pt[0],pt[1]))
        
        if inner == []:
            pass
        else:
            for r in inner:
                ring = []
                for pt in r:
                    if len(pt) == 3:
                        ring.append(Point(pt[0],pt[1],pt[2]))
                    elif len(pt) == 2:
                        ring.append(Point(pt[0],pt[1]))
                self.innercoords.append(ring)
            self.irings = len(inner)
    
    
    def toMySQL_polygon(self):
        # Begin MySQL Polygon output
        output = 'POLYGON('
        
        # Start outer ring output
        output += '('
        
        # For each point in coordinates, add to output
        for pt in self.outercoords:
            output += pt.toMySQLcoords() + ","
        
        # Strip last comma from output and close outer ring
        output = output[:-1] + ")"
        
        if self.irings > 0:
            # For each inner ring, add to output
            for n in range(self.irings):
                # Start output
                output += ",("
                
                # For each point in coordinates, add to output
                for pt in self.innercoords[n]:
                    output += pt.toMySQLcoords() + ","
                
                # Strip last comma from output and close ring
                output = output[:-1] + ")"
        
        # End Polygon output
        output += ')'
        return output
    
    
    def toKML(self,height=100,altmode="relativeToGround",extrude="yes"):
        # Start polygon output
        output = '<Polygon>\n'
        
        # Import KML Options Dictionaries
        import KMLOptions
        
        # Get extrude option
        output += KMLOptions.extrude.get(extrude)
        
        # Get altitude mode
        output += KMLOptions.altitudeMode.get(altmode)
        
        # Add outer ring to output
        output += '<outerBoundaryIs>\n'
        output += '<LinearRing>\n'
        output += '<coordinates>'
        
        # Add outer ring coordinates to output
        for pt in self.outercoords:
            pt.setElev(height)
            output += pt.toKMLcoords() + " "
        
        output += '</coordinates>\n'
        output += '</LinearRing>\n'
        output += '</outerBoundaryIs>\n'
        
        # Add inner rings to output if at least one exists
        if self.irings != None:
            for n in range(self.irings):
                output += '<innerBoundaryIs>\n'
                output += '<LinearRing>\n'
                output += '<coordinates>'
                
                # Add outer ring coordinates to output
                for pt in self.innercoords[n]:
                    pt.setElev(height)
                    output += pt.toKMLcoords() + " "
                
                output += '</coordinates>\n'
                output += '</LinearRing>\n'
                output += '</innerBoundaryIs>\n'
        
        # End KML Polygon output
        output += '</Polygon>\n'
        
        # Return formatted KML Polygon
        return output
    
    
    def toPointList(self):
        return { "outer" : self.outercoords , "inner" : self.innercoords }
    
    
    def segmentIntersect(self,segment):
        ''' Derived from: http://www.bryceboe.com/2006/10/23/line-segment-intersection-algorithm/ '''
        for v in range(len(polygon)-1):
            # Retrieve set of points for line segments
            A = edge[0]
            B = edge[1]
            C = polygon[v]
            D = polygon[v+1]
            
            # List of test values
            t = []
            t.append((D[1]-A[1])*(C[0]-A[0]))
            t.append((C[1]-A[1])*(D[0]-A[0]))
            t.append((D[1]-B[1])*(C[0]-B[0]))
            t.append((C[1]-B[1])*(D[0]-B[0]))
            t.append((C[1]-A[1])*(B[0]-A[0]))
            t.append((B[1]-A[1])*(C[0]-A[0]))
            t.append((D[1]-A[1])*(B[0]-A[0]))
            t.append((B[1]-A[1])*(D[0]-A[0]))
            
            # Test for intersection
            if t[0] > t[1] != t[2] > t[3] and t[4] > t[5] != t[6] > t[7]:
                # If intersection detected, return True
                return True
        
        # If no intersection detected, return false
        return False
    
    
    def containsPoint(self,point):
        '''
        Adapted from code found at: http://www.ariel.com.au/a/python-point-int-poly.html
        '''
        
        x = float(point.lon)
        y = float(point.lat)
                
        n = len(self.outercoords)
        inside = False
    
        p1x = float(self.outercoords[0].lon)
        p1y = float(self.outercoords[0].lat)
        
        for i in range(n+1):
            p2x = float(self.outercoords[i % n].lon)
            p2y = float(self.outercoords[i % n].lat)
            
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        
        return inside
    
    
    def segments(self,p):
        ''' Helper function for calculating area '''
        return zip(p, p[1:] + [p[0]])
    
    
    def calcArea(self,coords):
        ''' Helper function for calculating area in square meters '''
        # Initialize variables
        area = 0.0
        points = []
        startpt = None
        
        # Convert coordinates to metric
        for pt in coords:
            # If no start point set, set start point and add (0,0)
            if startpt == None:
                startpt = pt
                points.append( (0.0,0.0) )
            else:
                # Get distance between vertices
                dist = pt.distanceFrom(startpt)
                x = float(dist["horiz"])
                y = float(dist["vertical"])
                
                # Adjust distances in the correct direction
                if pt.lon < startpt.lon:
                    x *= -1
                if pt.lat < startpt.lat:
                    y *= -1
                
                # Create metric point
                metricPt = (x,y)
                
                # If point not already in points, add to point list
                if not metricPt in points:
                    points.append( metricPt )
        
#        # Calculate number of points
#        n = len(points)
        area =  0.5 * abs(sum( [ x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in self.segments(points) ] ))
        return area
        
#        # For each vertex (implementation of Green's theorem
#        for i in range(0,n-1):
#            j = (i+1) % n
#            area += points[i][0] * points[j][1]
#            area -= points[i][1] * points[j][0]
#        
#        # Return calculated area
#        return area/2.0
    
    
    def calcPerimeter(self,coords):
        ''' Helper function for calculating perimeter in meters '''
        # Initialize variables
        perimeter = 0.0
        prevpt = None
        # Loop through points to get perimeter
        for pt in coords:
            # If no previous point set, set previous point
            if prevpt == None:
                prevpt = pt
            else:
                # Get distance between vertices and add to perimeter
                perimeter += pt.distanceFrom(prevpt)["total"]
                # Adjust distances in the correct direction
                prevpt = pt
        # Return perimeter
        return perimeter
    
    
    def area(self):
        ''' Calculate polygon area (square meters) '''
        area = 0.0
        # Get outer coordinates containment area
        area += self.calcArea(self.outercoords)
        # If no internal rings, use only outer coordinates
        if self.irings == None:
            pass
        else:
            # Subtract inner ring area from total area
            area -= sum( [ self.calcArea(ring) for ring in innercoords ] )
        # Return area (units: square meters)
        return area
    
    
    def perimeter(self):
        ''' Calculate polygon perimeter (meters) '''
        perimeter = 0.0
        # Get outer coordinates containment area
        perimeter += self.calcPerimeter(self.outercoords)
        # If no internal rings, use only outer coordinates
        if self.irings == None:
            pass
        else:
            # Subtract inner ring area from total area
            perimeter += sum( [ self.calcPerimeter(ring) for ring in innercoords ] )
        # Return area (units: square meters)
        return perimeter



# Class for storing paths
#   coords - list of point dictionaries
class Path:
    '''
    Class for storing path features
    
        Storage variables:
            coords - list of path coordinates as Point objects
        
        Methods:
            numCoords()
            length()
            fromMySQL_linestring(mysql)
            fromKML(kml)
            fromPointList(coord)
            toKML(height,altmode,extrude)
            toMySQL_linestring()
    '''
    
    def __init__(self):
        self.coords = []
    
    
    def numCoords(self):
        ''' Return number of coordinates in path '''
        return len(self.coords)
    
    
    def length(self):
        ''' Calculate path length in meters '''
        # Initialize path length variable
        pathLen = 0.
        prevpt = None
        # For each point, get distance from previous point and add to total length
        for pt in self.coords:
            # If previous point not set, set to current point and continue
            if prevpt == None:
                prevpt = pt
            else:
                # Add distance from current point to previous point to total length
                pathLen += pt.distanceFrom(prevpt)["total"]
                # Set current point to previous point
                prevpt = pt
        # Return total path length
        return pathLen
    
    
    def fromMySQL_linestring(self,mysql):
        ''' Create path from MySQL linestring '''
        # Strip LINESTRING from MySQL format LINESTRING(points)
        i = str(mysql).replace('LINESTRING(','').replace(')','').split(',')
        
        # Process coordinates
        for p in i:
            lon,lat = p.split(" ")
            self.coords.append(Point(lon,lat))
    
    
    def fromKML(self,kml):
        ''' Create path from KML '''
        # Import XML parser
        from xml.dom.minidom import parseString
        
        # Parse KML input
        parsedKML = parseString(kml)
        
        # Get coordinates
        co = parsedKML.getElementsByTagName("outerBoundaryIs")[0].getElementsByTagName("coordinates")[0].firstChild.nodeValue.strip().split(" ")
        for coord in co:
            lon,lat,elev = coord.split(",")
            self.coord.append(Point(lon,lat,elev))
    
    
    def fromPointList(self,coord):
        ''' Create path from point list '''
        for pt in coord:
            if len(pt) == 3:
                self.coords.append(Point(pt[0],pt[1],pt[2]))
            elif len(pt) == 2:
                self.coords.append(Point(pt[0],pt[1]))
    
    
    def toKML(self,height=0,altmode="clampToGround",extrude="yes"):
        ''' Output path as KML '''
        # Begin LineString output
        output = '<LineString>\n'
        
        # Import KML Options Dictionaries
        import KMLOptions
        
        # Get extrude option
        output += KMLOptions.extrude.get(extrude)
        
        # Get altitude mode
        output += KMLOptions.altitudeMode.get(altmode)
        
        # Begin coordinate output
        output += '<coordinates>'
        
        # Process coordinates
        for pt in self.coords:
            pt.setElev(height)
            output += pt.toKMLcoords() + " "
        
        # End coordinate output
        output += '</coordinates>\n'
        
        # End LineString output
        output += '</LineString>\n'
        
        # Return formatted KML LineString
        return output
    
    
    def toMySQL_linestring(self):
        ''' Output path as MySQL linestring '''
        # Start output
        output = 'LINESTRING('
        
        # For each point, append 
        for pt in self.coords:
            output += pt.toMySQLcoords() + ","
        
        # Strip last comma and end output
        output = output[:-1] + ')'
        
        # Return formatted MySQL LineString
        return output



