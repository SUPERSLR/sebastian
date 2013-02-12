#!/usr/bin/python
# Keith Mosher
# sebastian/model/berm_model.py
# Optimization model for Port Protector berm design

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


# Connect to main database
DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')

# Connect to elevation database
elevDBhandle = GeoUtils.RDB()
elevDBhandle.connect('uws_maps')
#elevDBhandle.setHost(GeoUtils.constants.AmazonDBHost)
#elevDBhandle.connect('uws_ge')


def makeNetwork(pid,w=1,h=1,eq=GeoUtils.constants.Equations.BMASW,elev_data=GeoUtils.constants.ElevSrc.DEFAULT30SEC):
    '''
    Create network from elevation grid

    Parameters:
        @param pid - port ID
        @param w - grid width in degrees (default: 1)
        @param h - grid height in degrees (default: 1)
        @param eq - design equation as constant in GeoUtils.constants.Equations (default: SUPERSLR Minimum-Criteria Dike Design)
        @param elevdata - elevation data to use for grid as constant in GeoUtils.constants.ElevSrc (default: 30-second SRTM30Plus)

    '''
    # Query database for port details
    portq = "SELECT ID,name,latitude,longitude FROM portdata WHERE ID='%s'" % (pid,)
    portdata,portrowcount = DBhandle.query(portq)

    # If not only one port returned from database, raise error
    if portrowcount == 0 or portrowcount > 1:
        # Return error
        errtxt = "There was an error while retrieving the port data. <br/><br/>\n"
        errtxt += "Please report this error to %s " % (GeoUtils.constants.contactEmail,)
        errtxt += "including the following information: "
        errtxt += "Port ID - %s, Number of ports - %s" % (pid,portrowcount)

        # Return error text and error
        # Function exits
        return errtxt,True

    # Get port latitude and longitude
    port_lat = float(portdata[0]['latitude'])
    port_lon = float(portdata[0]['longitude'])

    # Determine bounding box for area of interest surrounding port
    west = float(port_lon) - float(w) / 2
    east = float(port_lon) + float(w) / 2
    north = float(port_lat) + float(h) / 2
    south = float(port_lat) - float(h) / 2

    print "Grid info: latitude: %s, longitude: %s, h: %s, w: %s, dataset: %s" % (port_lat,port_lon,h,w,elev_data,)
    print "Bounding west: %s, east: %s, north %s, south %s" % (west,east,north,south,)

    # Create bounding polygon syntax for SQL
    boundingPoly = "PolyFromText('%s')" % (GeoUtils.makeBoundingPolygon(north,south,east,west),)

    # Query database for associated port polygons
    polyq = "SELECT ID,AsText(feature_geometry) FROM current_features WHERE "
    #polyq += "(feature_type = 'Port Infrastructure Polygon' OR feature_type = 'Model Avoid Polygon') "
    polyq += "(feature_type = 'Port Infrastructure Polygon' OR feature_type = 'Berm Avoid Polygon') "
    polyq += "AND MBRIntersects(%s,feature_geometry)" % (boundingPoly,)
    polydata,polyrowcount = DBhandle.query(polyq)

    # Query database for associated port polygons
    seq = "SELECT ID,AsText(feature_geometry) FROM current_features WHERE "
    seq += "feature_type = 'Model StartEnd Polygon' "
    seq += "AND MBRIntersects(%s,feature_geometry)" % (boundingPoly,)
    sedata,serowcount = DBhandle.query(seq)

    elev_table_name,error = GeoUtils.constants.getShardTable(port_lat,port_lon,elev_data)
    #print "makeNetwork: elev_table_name %s, %s" % (elev_table_name,error,)
    # If there was an error, return error and message
    if error == True:
        errtxt = elev_table_name
        # Function exits
        return errtxt,True

    elevq = "SELECT longitude,latitude,elevation FROM "
    elevq += elev_table_name
    elevq += " WHERE "
    elevq += "longitude <= %s AND longitude >= %s AND latitude <= %s AND latitude >= %s AND source='%s' ORDER BY latitude, longitude ASC" % \
        (east,west,north,south,elev_data)

    elevdata,elevrowcount = elevDBhandle.query(elevq)

    # If there are results from the database, process elevation grid
    if elevrowcount == 0:
        # Return error message
        errtxt = "There was an error while retrieving the elevation grid. "
        errtxt += "The elevation data may not currently be loaded in the database. <br/><br/>"
        errtxt += "Please report this error to %s " % (GeoUtils.constants.contactEmail,)
        errtxt += "along with the following information: Port ID - %s" % (pid,)

        # Return error text and error
        # Function exits
        return errtxt,True

    # Import design cost functions
    import designs

    # Dictionary of possible cross-section equations
    eqns = {
            GeoUtils.constants.Equations.KMB2 : designs.pieceByPiece,
            GeoUtils.constants.Equations.BMASW : designs.pieceByPiece,
            GeoUtils.constants.Equations.SMCDD : designs.SMCDD
        }

    # Query database for global parameters
    gpq = "SELECT * FROM modelparameters WHERE eqn = '%s'" % (eq,)
    gpdata,gprowcount = DBhandle.query(gpq)

    # Query database for local parameters
    lpq = "SELECT mean_low_low_tide,mean_high_high_tide,storm_surge,design_wave_height "
    lpq += "FROM portdata WHERE ID = '%s'" % (pid,)
    lpdata,lprowcount = DBhandle.query(lpq)

    # Process global parameters database result
    # If more than one record returned or no records returned, raise error
    if gprowcount == 0 or gprowcount > 1:
        # Return error
        errtxt = "There was an error while retrieving the global port protector parameters.<br/><br/>y\n"
        errtxt += "Please report this error to %s, " % (GeoUtils.constants.contactEmail,)
        errtxt += "including the information below.\n\n"
        errtxt += "Port ID: %s\n" % (pid,)
        errtxt += "Design equation: %s\n" % (eq,)
        errtxt += "Number of global parameter rows: %s\n" % (gprowcount,)
        errtxt += "Number of local parameter rows: %s\n" % (lprowcount,)

        # Return error text and error
        # Function exits
        return errtxt,True

    # Set parameters to global values
    params = gpdata[0]

    # Only work with localized parameters if only one set is returned
    if lprowcount == 1:
        # Search for localized parameters, if exists and different from global value,
        #   set parameter to localized value
        for i in params:
            if not lpdata[0].has_key(i) or lpdata[0][i] == "-9999" or lpdata[0][i] == -9999 or lpdata[0][i] == params[i]:
                continue
            else:
                params[i] = lpdata[0][i]

    # Get initial point
    initPt = GeoUtils.Features.Point(x=float(elevdata[0]['longitude']),y=float(elevdata[0]['latitude']),elev=float(elevdata[0]['elevation']))

    # Select elevation grid size based on elevation data source
    dr = GeoUtils.constants.ElevSize.get(elev_data)

    #print "make network starting grid"
    # Get local distance between points
    distDiffInit = initPt.distanceFrom(GeoUtils.Features.Point(x=initPt.lon+dr,y=initPt.lat+dr))
    #distDiffInit = initPt.distanceFrom(GeoUtils.Features.Point(x=initPt.lon+0.003,y=initPt.lat+0.003))

    # Dictionary for grid vertices
    grid = {}

    for r in elevdata:
        # Create new Point based on database record
        curPt = GeoUtils.Features.Point(x=float(r['longitude']),y=float(r['latitude']),elev=float(r['elevation']))

        # Get metric distances from initial point
        distCurInit = curPt.distanceFrom(initPt)

        # Convert to integer coordinates on grid
        IntCoordX = int(round(distCurInit["horiz"] / distDiffInit["horiz"],0))
        IntCoordY = int(round(distCurInit["vertical"] / distDiffInit["vertical"],0))
        GridCoord = (IntCoordX,IntCoordY)

        # Store raw metric coordinates and elevation at integer coordinate on grid
        grid[GridCoord] = {
                "latlon" : (curPt.lon,curPt.lat),
                "metric" : (distCurInit["horiz"],distCurInit["vertical"]),
                "elev" : curPt.elev
            }

    #print "make network finished grid"
    #print grid
    # List of keys to delete because of avoid polygons or parameter exclusion
    del_keys = []

    # If there is one or more avoid polygons, delete vertices inside these polygons
    if polyrowcount > 0:
        # For each avoid polygon, if vertex lies within polygon, add to list of keys to be deleted
        for polygon in polydata:
            poly = GeoUtils.Features.Polygon()
            poly.fromMySQL_polygon(polygon['AsText(feature_geometry)'])
            del_keys.extend([ v for v in grid if poly.containsPoint(GeoUtils.Features.Point(x=grid[v]["latlon"][0],y=grid[v]["latlon"][1])) ])

    # Add vertices excluded by parameters to delete list
    #   Current disqualifying parameters: max_elevation, min_elevation
    del_keys.extend([ v for v in grid if grid[v]["elev"] > float(params['max_elevation']) or grid[v]["elev"] < float(params['min_elevation']) ])

    # Delete listed keys from available vertices
    for v in del_keys:
        if v in grid:
            del grid[v]

    # Process start/end points
    # If two start end polygons in immediate vicinity, use these regions for starting and ending points
    if serowcount == 2:
        # Start and end polygons
        startpoly = GeoUtils.Features.Polygon()
        startpoly.fromMySQL_polygon(sedata[0]['AsText(feature_geometry)'])
        endpoly = GeoUtils.Features.Polygon()
        endpoly.fromMySQL_polygon(sedata[1]['AsText(feature_geometry)'])

        # Check vertices for appropriate inclusion in start and end points
        spts = [ v for v in grid if startpoly.containsPoint(GeoUtils.Features.Point(x=grid[v]["latlon"][0],y=grid[v]["latlon"][1])) ]
        epts = [ v for v in grid if endpoly.containsPoint(GeoUtils.Features.Point(x=grid[v]["latlon"][0],y=grid[v]["latlon"][1])) ]
    else:
        # Return error message
        errtxt = "There was an error while retrieving the starting and ending polygons.<br/><br/>\n"
        errtxt += "Please ensure that there are exactly two StartEnd Polygons in the prescribed grid "
        errtxt += "and that each polygon contains possible grid points.<br/><br/>\n"
        errtxt += "Please report this error to %s " % (GeoUtils.constants.contactEmail,)
        errtxt += "along with the following information:\n"
        errtxt += "Port ID - %s\n" % (pid,)
        errtxt += "SE Polygons returned - %s\n" % (serowcount,)

        # Return error text and error
        # Function exits
        return errtxt,True


    # Dictionary to store graph
    graph = {}

    # Create network based on vertices
    for vertex in grid:
        # Create directory for edges
        graph[vertex] = {}
        # Get grid x and y for current vertex
        x,y = vertex
        # Neighbors of current vertex
        neighbors = [
                (x,y + 1),
                (x,y - 1),
                (x - 1,y),
                (x - 1,y + 1),
                (x - 1,y - 1),
                (x + 1,y),
                (x + 1,y + 1),
                (x + 1,y - 1)
            ]

        # For each neighbor, check for key and compute cost based on distance and average elevation
        for neighbr in neighbors:
            if grid.has_key(neighbr):
                # Calculate distance between current vertex and neighbor
                vertexPt = GeoUtils.Features.Point(x=grid[vertex]["latlon"][0],y=grid[vertex]["latlon"][1])
                nighbrPt = GeoUtils.Features.Point(x=grid[neighbr]["latlon"][0],y=grid[neighbr]["latlon"][1])
                dist = vertexPt.distanceFrom(nighbrPt)

                # Calculate average elevation
                avg_elev = (float(grid[vertex]["elev"]) + float(grid[neighbr]["elev"])) / 2

                # Get cost for edge
                graph[vertex][neighbr] = eqns.get(eq)(dist["total"],avg_elev,params)

    # List of edges to delete
    #del_edges = []

    # For each avoid polygon, if edges intersects with polygon, add to list of edges to be deleted
    #for polygon in polydata:
    #    poly = GeoMySQL.poly2coords(polygon['AsText(feature_geometry)'])["outer"]
    #    for v in graph:
    #        for e in graph[v]:
    #            edge = (grid[v]["latlon"],grid[e]["latlon"])
    #            if edgeintersectpoly(edge,poly):
    #                del_edges.append((v,e))

    # Delete listed edges from graph
    #for e in del_edges:
    #    if e[0] in graph:
    #        if e[1] in graph[e[0]]:
    #            pass
    #            #del graph[e[0]][e[1]]
    #            #print e

    # Return graph and no error
    return (grid,graph,spts,epts,boundingPoly),False


# Run optimization
# pid - port ID
# w - grid width in degrees (Default: 1)
# h - grid height in degrees (Default: 1)
# eq - design cost equation to use (Default: SUPERSLR Minimum-Criteria Dike Design)
# elevdata - elevation data to use for grid (Default: 30-second SRTM30Plus grid)
def optimize(pid,w=1,h=1,eq=GeoUtils.constants.Equations.SMCDD,elevdata=GeoUtils.constants.ElevSrc.DEFAULT30SEC):
    '''
    Run Port Protector Optimization

    Parameters
        @param pid - port ID
        @param w - grid width in degrees (default: 1)
        @param h - grid height in degrees (default: 1)
        @param eq - design equation as constant in GeoUtils.constants.Equations (default: SUPERSLR Minimum-Criteria Dike Design)
        @param elevdata - elevation data to use for grid as constant in GeoUtils.constants.ElevSrc (default: 30-second SRTM30Plus)

    '''
    #print "<br/>Debug - optimize_01<br/>"
    # Get grid
    response,error = makeNetwork(int(pid),float(w),float(h),eq,elevdata)
    #print "<br/>Debug - optimize_02_1<br/>"
    ###print response
    ###print "<br/>Debug - optimize_02_2<br/>"
    # If there was an error, return error and message
    if error == True:
        errtxt = response
        # Function exits
        return errtxt,True
    # Unpack response
    #print "<br/>Debug - optimize_02_2<br/>"
    (grid,graph,startpts,endpts,bPoly) = response
    ###print "<br/>Debug - optimize_02_3<br/>"
    # Import shortest path algorithm
    import dijkstra
    # For each start point and end point
    optimalPaths = [ dijkstra.shortestPath(graph,start,end) for end in endpts for start in startpts ]
    #print "<br/>Debug - optimize_02_4<br/>"
    # Initialize minimum distance to infinity
    vol = float('inf')
    # Initialize shortest path to false
    sp = False
    # For each path and distance, check to determine if shortest
    for possiblePath in optimalPaths:
        print "possiblePath"
        if possiblePath == (False,False):
            pass
        elif float(possiblePath[1]) < vol:
            vol = float(possiblePath[1])
            sp = possiblePath[0]
        else:
            pass
    # Shortest path details variable holders
    path = []
    pts = []
    elev = []
    length = 0.0
    # Initialize volume variables
    dikeVol = 0.0
    toeVol = 0.0
    coreVol = 0.0
    armorVol = 0.0
    foundVol = 0.0
    totalVol = 0.0
    #print "<br/>Debug optimize_02<br/>"
###    print "<table border=1>"
###    print "<tr>"
    #print "<td>%f</td>" % (length, )
    #print "<td>%f</td><td>%f</td>" % (length, dikeVol, )
###    print "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % ('length', 'dikeVol', 'toeVol', 'coreVol', 'armorVol', 'foundVol', 'totalVol', )
###    print "</tr><tr>"
###    print "<td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td>" % (length, dikeVol, toeVol, coreVol, armorVol, foundVol, totalVol, )

    try:
        prev = False
        for v in sp:
            print "checking path"
###            print "</tr><tr><td colspan=7>%s</td></tr><tr>" % (prev, )
            # add up incremental volumes
            if (eq == GeoUtils.constants.Equations.BMASW or eq == GeoUtils.constants.Equations.SMCDD) and prev:
###                print "</tr><tr><td colspan=7>%s</td></tr><tr>" % (graph[prev][v], )
                dikeVol += graph[prev][v]['dikeVol']
                toeVol += graph[prev][v]['toeVol']
                coreVol += graph[prev][v]['coreVol']
                foundVol += graph[prev][v]['foundVol']
                armorVol += graph[prev][v]['armorVol']
                totalVol += graph[prev][v]['cost']
###                print "</tr><tr>"
###                print "<td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td>" % (length, dikeVol, toeVol, coreVol, armorVol, foundVol, totalVol, )
            # Add point details to paths
            path.append(grid[v]["latlon"])
            pts.append(grid[v]["metric"])
            elev.append(float(grid[v]["elev"]))
            # Set previous point to current point
            prev = v

    except TypeError:
        # Build error message
        msg = '<h3>Error:</h3>\n'
        msg += '<p>No optimal paths found, please change your parameters and try again.</p>\n<br/><br/>\n'
        msg += '<p>Debugging information (TypeError):<br/>%s</p>\n' % (sp,)
        # Output error message
        output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)
        # Return error and message
        # Function exits
        return output,True

###    print "</tr>"
###    print "</table>"

    # Average elevation along path
    avg_elev = sum(elev) / len(elev)

    #placeholder for the processed values of materials

    riprap_volume = -2
    aggregate_volume = -2
    rebar_volume = -2
    cement_volume = -2
    riprap_weight = -2
    aggregate_weight = -2
    rebar_weight = -2
    cement_weight = -2


    # Prepare values used to update database
    output = (path,avg_elev,totalVol,dikeVol,coreVol,toeVol,foundVol,armorVol,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight)
    # Return output and no error
    return output,False


# Update database
def updateDB(ge_key,pid,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight,eq,elevdata,computeCenter,grid_height,grid_width):
    #print 'updateDB running'
    '''
    Update database with berm_model result

    Parameters
        @param ge_key - user's identifying key
        @param pid - port ID
        @param path - Path object to store in database
        @param avg_elev - average path elevation
        @param vol - total path volume
        @param dikeVol - dike volume
        @param coreVol - core volume
        @param toeVol - toe volume
        @param foundVol - foundation volume
        @param armorVol - armor volume
        @param eq - design equation used to calculate path as constant in GeoUtils.constants.Equations
        @param elevdata - elevation dataset used for grid as constant in GeoUtils.constants.ElevSrc
        @param computeCenter - computation center where calculation was performed as retrieved from GeoUtils.constants.computeCenter()
        @param grid_height - height of grid used to calculate path
        @param grid_width - width of grid used to calculate path

    '''
    # Get current user details
    DBhandle.setConnUserKey(ge_key)
    user = DBhandle.ConnUserName()

    # Delete old model run and insert into history
    selq = 'SELECT portID,timestamp,attribution,avg_elev,path_length,path_volume,dike_volume,core_volume,toe_volume,foundation_volume,armor_volume,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight,AsText(path_geometry),3Dfile,equation,elev_data,computeCenter,grid_height,grid_width FROM berm_model WHERE '
    selq += 'portID=%s' % (pid)
    seldata,selrc = DBhandle.query(selq)

    for r in seldata:
        histq = "INSERT INTO berm_model_history (portID,created,attribution,avg_elev,path_length,path_volume,dike_volume,core_volume,toe_volume,foundation_volume,armor_volume,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight,path_geometry,3Dfile,equation,elev_data,computeCenter,grid_height,grid_width) VALUES ('"
        histq += "%(portID)s','%(timestamp)s','%(attribution)s','%(avg_elev)s','%(path_length)s','%(path_volume)s','%(dike_volume)s','%(core_volume)s','%(toe_volume)s','%(foundation_volume)s','%(armor_volume)s','%(riprap_volume)s','%(aggregate_volume)s','%(rebar_volume)s','%(cement_volume)s','%(riprap_weight)s','%(aggregate_weight)s','%(rebar_weight)s','%(cement_weight)s',PolyFromText('%(AsText(path_geometry))s'),'%(3Dfile)s','%(equation)s','%(elev_data)s','%(computeCenter)s','%(grid_height)s','%(grid_width)s')" % r
###        print histq
        histdata,histrc = DBhandle.query(histq)

    #delq = 'DELETE FROM portprotector WHERE MBRIntersects(' + bPoly + ',path_geometry)'
    delq = 'DELETE FROM berm_model WHERE portID=%s' % (pid)
    deldata,delrc = DBhandle.query(delq)

    # Create path for linestring creation
    ShortestPath = GeoUtils.Features.Path()
    ShortestPath.fromPointList(path)

    # Insert shortest path and volume into database
    insertq = "INSERT INTO berm_model (portID,attribution,avg_elev,path_length,path_volume," +\
            "dike_volume, core_volume, toe_volume, foundation_volume, armor_volume,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight," +\
            "path_geometry,3Dfile,equation,elev_data,computeCenter,grid_height,grid_width) "
    insertq += "VALUES ('%s','%s','%s','%s','%s'," % (pid,user,avg_elev,ShortestPath.length(),vol)
    insertq += "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " % (dikeVol, coreVol, toeVol, foundVol, armorVol,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight)
    insertq += "PolyFromText('%s'),'','%s','%s','%s','%s','%s')" % (ShortestPath.toMySQL_linestring(),eq,elevdata,computeCenter,grid_height,grid_width)
###    print insertq
    insertdata,insertrc = DBhandle.query(insertq)

    # Return success and no error
    return True,False
    # Return path and error to force path printing (for debugging)
    #return path,True



# If called directly, run with given query string parameters
if __name__ == "__main__":
    # Import cgi module to get query string
    import cgi

    try:
        # Get query string
        qv = cgi.FieldStorage()

        ge_key = qv["GE_KEY"].value
        pid = qv["PortID"].value
        w = qv["GridWidth"].value
        h = qv["GridHeight"].value
        eq = qv["Equation"].value
        elevdata = qv["ElevationData"].value
    except KeyError:
        ge_key = '14b9055d351595cc332c92eec2a06ebf'
        pid = 63
        w = .25
        h = .25
        eq = GeoUtils.constants.Equations.NTC_CS
        elevdata = GeoUtils.constants.ElevSrc.DEFAULT30SEC


    # Print content-type header
    print GeoUtils.Interface.ContentType("html")
    print

    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
    print "Debug"
    try:
        # Import time module to record runtime
        import time

        # Start clock
        StartTime = time.time()

        # Run optimization to obtain shortest path
        response,error = optimize(pid=pid,w=w,h=h,eq=eq,elevdata=elevdata)

        # Stop clock
        EndTime = time.time()

        # Elapsed time
        ElapsedTime = EndTime - StartTime

        if error == True:
            # Output error message
            output = GeoUtils.Interface.uniForm.fullErrorMsgGen(response)
            print output
        else:
            # Unpack response from optimization
            path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight = response

            # Update database
            response,error = updateDB(ge_key,pid,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight,eq,elevdata,GeoUtils.constants.computeCenter(),h,w)

            if error:
                # Output error message
                msg = "<h3>Error:</h3>\n<p>There was an error updating the database. Please try again.</p>"
                output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)
                print output
            else:
                # Output success message
                msg = '<h3>Success:</h3>\n<p>Please refresh your window to view the result.</p>\n'
                msg += '<br/><p>Model runtime: %f seconds</p>\n' % (ElapsedTime,)
                output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)
                print output
    except:
        import sys,traceback
        print 'Unexpected error:<br/><br/>\n<pre>\n%s\n</pre>\n<br/>\n\n' % (traceback.format_exc(),)

    print GeoUtils.Interface.StdHTMLFooter()

    # Close database
    DBhandle.close()

