#!/usr/bin/python
# Keith Mosher
# sebastian/model/berm_model.py
# Optimization model for Port Protector berm design

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
    import time
    startMakeNetworkTime = time.time()
    print "makeNetwork, current time: %s, elapsed time: %s" % (time.time(), startMakeNetworkTime-time.time())
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
            GeoUtils.constants.Equations.KMB2 : designs.multiDikeSingleBermCombo,
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

    print "makeNetworkx, pre-grid, current time: %s" % (startMakeNetworkTime -time.time())

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

    print "make networkx finished grid, number of points: %s" % (len(graph))
    print "makeNetworkx, post-grid, pre-find-delete-avoid, current time: %s" % (startMakeNetworkTime-time.time())
    #print grid
    # List of keys to delete because of avoid polygons or parameter exclusion
    del_keys = []

    # If there is one or more avoid polygons, delete vertices inside these polygons
    if polyrowcount > 0:
        # For each avoid polygon, if vertex lies within polygon, add to list of keys to be deleted
        for polygon in polydata:
            poly = GeoUtils.Features.Polygon()
            poly.fromMySQL_polygon(polygon['AsText(feature_geometry)'])
            del_keys.extend([ v for v in graph.nodes(data=False) if poly.containsPoint(GeoUtils.Features.Point(x=graph.node[v]["latlon"][0],y=graph.node[v]["latlon"][1])) ])

    print "makeNetwork, post-find-delete-avoid, pre-find-delete-depth/elev,current time: %s" % (startMakeNetworkTime-time.time())

    print "min elevation: %s" % (params['min_elevation'])
    print "max elevation: %s" % (params['max_elevation'])
    print "min elevation_berm: %s" % (params['min_elevation_berm'])
    print "max elevation_berm: %s" % (params['max_elevation_berm'])
    # Add vertices excluded by parameters to delete list
    #   Current disqualifying parameters: max_elevation_berm, min_elevation_berm
    del_keys.extend([ v for v in grid if grid[v]["elev"] > float(params['max_elevation_berm']) or grid[v]["elev"] < float(params['min_elevation_berm']) ])

    print "makeNetwork, post-find-delete-depth/elev, pre-actual-delete, current time: %s" % (startMakeNetworkTime-time.time())

    # Delete listed keys from available vertices
    for v in del_keys:
        if v in graph:
#            del graph[v]["latlon"]
#            del graph[v]["metric"]
#            del graph[v]["elev"]
            graph.remove_node(v)

    print "makeNetwork, post--actual-delete, current time: %s" % (startMakeNetworkTime-time.time())

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


        print "spts count: %s, pre-selecting 1" % (len(spts))
        print "epts count: %s, pre-selecting 1" % (len(epts))
        current_elev = -9999
        best_spt_v = 0
        for v in spts :
#            print "spts v: %s elev: %s" % (v,grid[v]["elev"])
            if grid[v]["elev"] > current_elev :
                current_elev = grid[v]["elev"]
                best_spt_v = v

        current_elev = -9999
        best_ept_v = 0
        for v in epts :
#            print "epts v: %s elev: %s" % (v,grid[v]["elev"])
            if grid[v]["elev"] > current_elev :
                current_elev = grid[v]["elev"]
                best_ept_v = v

        if best_spt_v <> 0 :
            print "best spt: %s %s" % (best_spt_v,grid[best_spt_v]["elev"])
            spts = [best_spt_v]
        if best_ept_v <> 0 :
            print "best ept: %s %s" % (best_ept_v,grid[best_ept_v]["elev"])
            epts = [best_ept_v]

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


    print "final number of grid points, after deletions: %s" % (len(graph))
    print "makeNetwork, pre-graph, current time: %s" % (startMakeNetworkTime-time.time())


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



    print "makeNetwork,complete, current time: %s" % (startMakeNetworkTime-time.time())
    # Return graph and no error
    return (graph,spts,epts,boundingPoly),False


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

    # Get grid
    response,error = makeNetwork(int(pid),float(w),float(h),eq,elevdata)

    # If there was an error, return error and message
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

    # Average elevation along path
    avg_elev = sum(elev) / len(elev)

    #placeholder for the processed values of materials
    riprap_volume = -1
    aggregate_volume = -1
    rebar_volume = -1
    cement_volume = -1
    riprap_weight = -1
    aggregate_weight = -1
    rebar_weight = -1
    cement_weight = -1


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
        histdata,histrc = DBhandle.query(histq)

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

    insertdata,insertrc = DBhandle.query(insertq)

    # Return success and no error
    return True,False



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

