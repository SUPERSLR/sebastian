#!/usr/bin/python
# David Newell
# sebastian/model/portprotector.py
# Optimization model for Port Protector design

# Import required modules
import sys, os

# Switch to custom-compiled Python interpreter
INTERP = os.path.join(os.environ['HOME'], 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Import Useful Modules
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Import graph handling tools
import networkx as nx


# Connect to database
DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')

elevDBhandle = GeoUtils.RDB()
elevDBhandle.setHost(GeoUtils.constants.AmazonHost)
elevDBhandle.connect('uws_ge')


# Retrieve elevation data grid from database and create network
# pid - Port ID
# w - grid width (Default: 1 degree)
# h - grid height (Default: 1 degree)
# eq - equation to use for generating edge costs (Default: Nathan Chase's cross-section)
# elev_data - elevation data to use for grid (Default: 30-second SRTM30Plus grid)
def makeNetwork(pid,w=1,h=1,eq=GeoUtils.constants.Equations.BMASW,elev_data=GeoUtils.constants.ElevSrc.DEFAULT30SEC):
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


    port_lat = float(portdata[0]['latitude'])
    port_lon = float(portdata[0]['longitude'])

    # Determine bounding box for area of interest surrounding port
    west = float(port_lon) - float(w) / 2
    east = float(port_lon) + float(w) / 2
    north = float(port_lat) + float(h) / 2
    south = float(port_lat) - float(h) / 2

    # Create bounding polygon syntax for SQL
    boundingPoly = "PolyFromText('%s')" % (GeoUtils.makeBoundingPolygon(north,south,east,west),)

    # Query database for associated port polygons
    polyq = "SELECT ID,AsText(feature_geometry) FROM current_features WHERE "
    polyq += "(feature_type = 'Port Infrastructure Polygon' OR feature_type = 'Model Avoid Polygon') "
    polyq += "AND MBRIntersects(%s,feature_geometry)" % (boundingPoly,)
    polydata,polyrowcount = DBhandle.query(polyq)

    # Query database for associated port polygons
    seq = "SELECT ID,AsText(feature_geometry) FROM current_features WHERE "
    seq += "feature_type = 'Model StartEnd Polygon' "
    seq += "AND MBRIntersects(%s,feature_geometry)" % (boundingPoly,)
    sedata,serowcount = DBhandle.query(seq)

    # Query database for elevation grid
    elevq = "SELECT longitude,latitude,elevation FROM elev_data WHERE "
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
            GeoUtils.constants.Equations.BMASW : designs.pieceByPiece
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

    # Get local distance between points
    distDiffInit = initPt.distanceFrom(GeoUtils.Features.Point(x=initPt.lon+dr,y=initPt.lat+dr))

    # Graph for processing model
    graph = nx.Graph()

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
        if not graph.has_node(GridCoord):
            graph.add_node(GridCoord,latlon=(curPt.lon,curPt.lat),
                                metric=(distCurInit["horiz"],distCurInit["vertical"]),
                                elev=curPt.elev)


    # List of keys to delete because of avoid polygons or parameter exclusion
    del_keys = []

    # If there is one or more avoid polygons, delete vertices inside these polygons
    if polyrowcount > 0:
        # For each avoid polygon, if vertex lies within polygon, add to list of keys to be deleted
        for polygon in polydata:
            poly = GeoUtils.Features.Polygon()
            poly.fromMySQL_polygon(polygon['AsText(feature_geometry)'])
            del_keys.extend([ v for v in graph.nodes(data=False) if poly.containsPoint(GeoUtils.Features.Point(x=graph.node[v]["latlon"][0],y=graph.node[v]["latlon"][1])) ])

    # Add vertices excluded by parameters to delete list
    #   Current disqualifying parameters: max_elevation, min_elevation
    del_keys.extend([ v for v in graph.nodes(data=False) if graph.node[v]["elev"] > float(params['max_elevation']) or graph.node[v]["elev"] < float(params['min_elevation']) ])

    # Delete listed keys from available vertices
    for v in del_keys:
        if v in graph:
#            del graph[v]["latlon"]
#            del graph[v]["metric"]
#            del graph[v]["elev"]
            graph.remove_node(v)

    # Process start/end points
    # If two start end polygons in immediate vicinity, use these regions for starting and ending points
    if serowcount == 2:
        # Start and end polygons
        startpoly = GeoUtils.Features.Polygon()
        startpoly.fromMySQL_polygon(sedata[0]['AsText(feature_geometry)'])
        endpoly = GeoUtils.Features.Polygon()
        endpoly.fromMySQL_polygon(sedata[1]['AsText(feature_geometry)'])

        # Check vertices for appropriate inclusion in start and end points
        spts = [ v for v in graph.nodes(data=False) if startpoly.containsPoint(GeoUtils.Features.Point(x=graph.node[v]["latlon"][0],y=graph.node[v]["latlon"][1])) ]
        epts = [ v for v in graph.nodes(data=False) if endpoly.containsPoint(GeoUtils.Features.Point(x=graph.node[v]["latlon"][0],y=graph.node[v]["latlon"][1])) ]
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


    # Create network based on vertices
    for v in graph:
        # Get grid x and y for current vertex
        x,y = v

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
        for k in neighbors:
            if graph.has_node(k):
                # Calculate distance between current vertex and neighbor
                ptV = GeoUtils.Features.Point(x=graph.node[v]["latlon"][0],y=graph.node[v]["latlon"][1])
                ptK = GeoUtils.Features.Point(x=graph.node[k]["latlon"][0],y=graph.node[k]["latlon"][1])
                dist = ptV.distanceFrom(ptK)

                # Calculate average elevation
                avg_elev = (float(graph.node[v]["elev"]) + float(graph.node[k]["elev"])) / 2

                # Get cost for edge
                weight,vars = eqns.get(eq)(dist["total"],avg_elev,params)

                # Add edge to graph is not
                if not graph.has_edge(v,k):
                    graph.add_edge(v,k,weight=weight,vars=vars)

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
    return (graph,spts,epts,boundingPoly),False


# Run optimization
# pid - port ID
# w - grid width in degrees (Default: 1)
# h - grid height in degrees (Default: 1)
# eq - design cost equation to use (Default: NTC Cross-Section)
# elevdata - elevation data to use for grid (Default: 30-second SRTM30Plus grid)
def optimize(pid,w="1",h="1",eq = GeoUtils.constants.Equations.BMASW, elevdata = GeoUtils.constants.ElevSrc.DEFAULT30SEC):
    # Get grid
    response,error = makeNetwork(int(pid),float(w),float(h),eq,elevdata)
    print "test optimize"
    if error == True:
        errtxt = response
        # Function exits
        return errtxt,True

    # Unpack response
    (graph,startpts,endpts,bPoly) = response

    # Dictionary of costs to paths
    SPs = {}

    # Run shortest path algorithm for each start point and end point
    for start in startpts:
        for end in endpts:
            path = nx.shortest_path(graph,source=start,target=end,weighted=True)
            vol = nx.shortest_path_length(graph,source=start,target=end,weighted=True)
            SPs[vol] = path

    # Find minimum volume
    minVol = min(SPs.keys())

    # Select shortest path based on minimum volume
    shortestPath = SPs[minVol]

    # Initialize piece volumes
    dikeVol = 0.0
    toeVol = 0.0
    coreVol = 0.0
    armorVol = 0.0
    foundVol = 0.0

    # Shortest path details variable holders
    path = []
    pts = []
    elev = []
    length = 0.0
    buckets = [];
    bucket_width = 5;
    for init_depth in xrange (0, max_depth + bucket_width, bucket_width):
        buckets[init_depth]=0



    # Calculate piece volumes and path lists
    for pt in range(0,len(shortestPath)):
        if pt > 0:
            dikeVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["dikeVol"]
            toeVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["toeVol"]
            coreVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["coreVol"]
            foundVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["foundVol"]
            armorVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["armorVol"]

        path.append(graph.node[shortestPath[pt]]["latlon"])
        pts.append(graph.node[shortestPath[pt]]["metric"])
        elev.append(float(graph.node[shortestPath[pt]]["elev"]))
        current_elev_bucket = round(float(graph.node[shortestPath[pt]]["elev"]) / bucket_width)
        buckets[current_elev_bucket] += float(graph.node[shortestPath[pt]]["vars"]["length"]);

    # Average elevation along path
    avg_elev = sum(elev) / len(elev)

    # Import math module for square roots
    import math

    for i in range(1,len(pts)):
        length += math.sqrt((float(pts[i][0]) - float(pts[i-1][0]))**2 + (float(pts[i][1]) - float(pts[i-1][1]))**2)

    # Prepare values used to update database
    output = (path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol, buckets)

    # Return output and no error
    return output,False


# Update database
def updateDB(ge_key,pid,path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,eq,elevdata,computeCenter,grid_height,grid_width):
    # Get current user details
    DBhandle.setConnUserKey(ge_key)
    user = DBhandle.ConnUserName()

    # Delete old model run and insert into history
    selq = 'SELECT portID,timestamp,attribution,avg_elev,path_length,path_volume,AsText(path_geometry),3Dfile,equation,elev_data,computeCenter,grid_height,grid_width FROM portprotector WHERE '
    selq += 'portID=%s' % (pid)
    seldata,selrc = DBhandle.query(selq)

    for r in seldata:
        histq = "INSERT INTO portprotector_history (portID,created,attribution,avg_elev,path_length,path_geometry,3Dfile,equation,elev_data,computeCenter,grid_height,grid_width) VALUES ('"
        histq += "%(portID)s','%(timestamp)s','%(attribution)s','%(avg_elev)s','%(path_length)s',PolyFromText('%(AsText(path_geometry))s'),'%(3Dfile)s','%(equation)s','%(elev_data)s','%(computeCenter)s','%(grid_height)s','%(grid_width)s')" % r
        histdata,histrc = DBhandle.query(histq)

    #delq = 'DELETE FROM portprotector WHERE MBRIntersects(' + bPoly + ',path_geometry)'
    delq = 'DELETE FROM portprotector WHERE portID=%s' % (pid)
    deldata,delrc = DBhandle.query(delq)

    # Create path for linestring creation
    ShortestPath = GeoUtils.Features.Path()
    ShortestPath.fromPointList(path)

    # Insert shortest path and volume into database
    insertq = "INSERT INTO portprotector (portID,attribution,avg_elev,path_length,path_volume," +\
                    "dike_volume, core_volume, toe_volume, foundation_volume, armor_volume," +\
                    "path_geometry,3Dfile,equation,elev_data,computeCenter,grid_height,grid_width) "
    insertq += "VALUES ('%s','%s','%s','%s','%s'," % (pid,user,avg_elev,length,vol)
    insertq += "'%s', '%s', '%s', '%s', '%s', " % (dikeVol, coreVol, toeVol, foundVol, armorVol)
    insertq += "PolyFromText('%s'),'','%s','%s','%s','%s','%s')" % (ShortestPath.toMySQL_linestring(),eq,elevdata,computeCenter,grid_height,grid_width)
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
        pid = 180
        w = .25
        h = .25
        eq = GeoUtils.constants.Equations.BMASW
        elevdata = GeoUtils.constants.ElevSrc.DEFAULT30SEC


    # Print content-type header
    print GeoUtils.Interface.ContentType("html")
    print

    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
    try:
        # Import time module to record runtime
        import time

        # Start clock
        StartTime = time.time()

        # Run optimization to obtain shortest path and length
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
            path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,buckets = response
            for init_depth in xrange (0, max_depth + bucket_width, bucket_width):
                print 'bucket size: %s bucket length: %s' % (init_depth, buckets[init_depth])

            # Update database
            response,error = updateDB(ge_key,pid,path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,eq,elevdata,GeoUtils.constants.computeCenter(),h,w)

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

