#!/usr/bin/python
# Keith Mosher
# sebastian/model/berm_model.py
# Optimization model for Port Protector berm design using networkx package

# Import required modules
import sys, os

# Switch to custom-compiled Python interpreter
#INTERP = os.path.join(os.environ['HOME'], 'bin', 'python')
#if sys.executable != INTERP:
#    os.execl(INTERP, INTERP, *sys.argv)

# Import Useful Modules
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



def makeNetwork(pid,w,h,eq,elev_data,run_type,current_structure):
#def makeNetwork(pid,w=1,h=1,eq=GeoUtils.constants.Equations.WBMAS,elev_data=GeoUtils.constants.ElevSrc.DEFAULT30SEC,run_type='networkx',current_structure='dike'):
    '''
    Create network from elevation grid

    Parameters:
        @param pid - port ID
        @param w - grid width in degrees (default: 1)
        @param h - grid height in degrees (default: 1)
        @param eq - design equation as constant in GeoUtils.constants.Equations (default: SUPERSLR Minimum-Criteria Dike Design)
        @param elevdata - elevation data to use for grid as constant in GeoUtils.constants.ElevSrc (default: 30-second SRTM30Plus)

    '''

    avoid_type= 'Model Avoid Polygon'
    max_elevation_parameter = 'max_elevation'
    min_elevation_parameter = 'min_elevation'
    if current_structure == 'berm' :
        avoid_type= 'Berm Avoid Polygon'
        max_elevation_parameter = 'max_elevation_berm'
        min_elevation_parameter = 'min_elevation_berm'

    import time
    startMakeNetworkTime = time.time()
    ###print "portprotector %s %s, dataset %s, starting time: %.3f" % (run_type,current_structure,elev_data,time.time())
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

    ###print "Grid info: latitude: %s, longitude: %s, h: %s, w: %s, dataset: %s" % (port_lat,port_lon,h,w,elev_data,)
    ###print "Bounding west: %s, east: %s, north %s, south %s" % (west,east,north,south,)

    # Create bounding polygon syntax for SQL
    boundingPoly = "PolyFromText('%s')" % (GeoUtils.makeBoundingPolygon(north,south,east,west),)

    # Query database for associated port or avoid polygons
    polyq = "SELECT ID,AsText(feature_geometry) FROM current_features WHERE "
    polyq += "(feature_type = 'Port Infrastructure Polygon' OR feature_type = '%s') " % (avoid_type,)
    # Commented to force avoid of all port polygons
    #polyq += "AND portID = '%s' " % (pid,)
    polyq += "AND MBRIntersects(%s,feature_geometry)" % (boundingPoly,)
    polydata,polyrowcount = DBhandle.query(polyq)

    # Query database for associated start or end port polygons
    seq = "SELECT ID,AsText(feature_geometry) FROM current_features WHERE "
    seq += "feature_type = 'Model StartEnd Polygon' "
    seq += "AND portID = '%s' " % (pid,)
    seq += "AND MBRIntersects(%s,feature_geometry)" % (boundingPoly,)
    sedata,serowcount = DBhandle.query(seq)

    # Process start/end points
    # If two start end polygons in immediate vicinity, use these regions for starting and ending points
    startpoly = GeoUtils.Features.Polygon()
    endpoly = GeoUtils.Features.Polygon()

    if serowcount == 2:
        # Start and end polygons
        startpoly.fromMySQL_polygon(sedata[0]['AsText(feature_geometry)'])
        endpoly.fromMySQL_polygon(sedata[1]['AsText(feature_geometry)'])

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

    elev_table_name,error = GeoUtils.constants.getShardTable(port_lat,port_lon,elev_data)

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
            GeoUtils.constants.Equations.KDBS : designs.dikeOrBermSection,
            GeoUtils.constants.Equations.WBMAS : designs.pieceByPiece,
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

    # Get local distance between points
    distDiffInit = initPt.distanceFrom(GeoUtils.Features.Point(x=initPt.lon+dr,y=initPt.lat+dr))

    # Dictionary for grid vertices
    grid = {}

    # Dictionary to store graph
    old_graph = {}

    # Graph for networkx points, empty until we know we can get the networkx library
    graph = None

    if run_type == 'old' :
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

        ###print "make network finished grid, number of points: %s, post-grid, pre-delete, elapsed time: %.3f" % (len(grid), time.time()-startMakeNetworkTime)

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
        del_keys.extend([ v for v in grid if grid[v]["elev"] > float(params[max_elevation_parameter]) or grid[v]["elev"] < float(params[min_elevation_parameter]) ])

        ###print "dike min/max elevation: %s / %s" % (params['min_elevation'],params['max_elevation'])
        ###print "berm min/max elevation: %s / %s" % (params['min_elevation_berm'], params['max_elevation_berm'])
        ###print "current parameters: %s / %s" % (min_elevation_parameter, max_elevation_parameter,)

        # Delete listed keys from available vertices
        for v in del_keys:
            if v in grid:
                del grid[v]

        # Process start/end points
        # Check vertices for appropriate inclusion in start and end points
        spts = [ v for v in grid if startpoly.containsPoint(GeoUtils.Features.Point(x=grid[v]["latlon"][0],y=grid[v]["latlon"][1])) ]
        epts = [ v for v in grid if endpoly.containsPoint(GeoUtils.Features.Point(x=grid[v]["latlon"][0],y=grid[v]["latlon"][1])) ]

        len_spts = len(spts)
        len_epts = len(epts)
        current_elev = -9999
        best_spt_v = 0
        for v in spts :
            if grid[v]["elev"] > current_elev :
                current_elev = grid[v]["elev"]
                best_spt_v = v

        current_elev = -9999
        best_ept_v = 0
        for v in epts :
            if grid[v]["elev"] > current_elev :
                current_elev = grid[v]["elev"]
                best_ept_v = v

        if best_spt_v <> 0 :
            ###print "spts count: %s, pre-selecting %s, elev: %s" % (len_spts,best_spt_v,grid[best_spt_v]["elev"])
            spts = [best_spt_v]
        if best_ept_v <> 0 :
            ###print "epts count: %s, pre-selecting %s, elev: %s" % (len_epts,best_ept_v,grid[best_ept_v]["elev"])
            epts = [best_ept_v]

        ###print "final number of grid points, after deletions: %s, post-delete, pre-graph, elapsed time: %.3f" % (len(grid),time.time()-startMakeNetworkTime,)

        # Create network based on vertices
        for vertex in grid:
            # Create directory for edges
            old_graph[vertex] = {}
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
                    old_graph[vertex][neighbr] = eqns.get(eq)(dist["total"],avg_elev,params)

        ###print "makeNetwork, graph-complete, function-complete, elapsed time: %.3f" % (time.time()-startMakeNetworkTime)

    elif run_type == 'networkx' :
        # Import graph handling tools
        import networkx as nx

        # Graph for processing model
        graph = nx.Graph()

        # Convert the points from the database from lat/lng to cartesian x/y
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

        ###print "makeNetworkx, post-grid, pre-delete, number of points: %s, elapsed time: %.3f" % (graph.number_of_nodes(), time.time()-startMakeNetworkTime)

        # List of keys to delete because of avoid polygons or parameter exclusion
        del_keys = []

        # If there is one or more avoid polygons, delete vertices inside these polygons
        if polyrowcount > 0:
            # For each avoid polygon, if vertex lies within polygon, add to list of keys to be deleted
            for polygon in polydata:
                poly = GeoUtils.Features.Polygon()
                poly.fromMySQL_polygon(polygon['AsText(feature_geometry)'])
                del_keys.extend([ v for v in graph.nodes(data=False) if poly.containsPoint(GeoUtils.Features.Point(x=graph.node[v]["latlon"][0],y=graph.node[v]["latlon"][1])) ])

        ###print "dike min/max elevation: %s / %s" % (params['min_elevation'],params['max_elevation'])
        ###print "berm min/max elevation: %s / %s" % (params['min_elevation_berm'], params['max_elevation_berm'])
        ###print "current parameters: %s / %s" % (min_elevation_parameter, max_elevation_parameter,)

        # Add vertices excluded by parameters to delete list
        #   Current disqualifying parameters: max_elevation_berm, min_elevation_berm
        del_keys.extend([ v for v in graph.nodes(data=False) if graph.node[v]["elev"] > float(params[max_elevation_parameter]) or graph.node[v]["elev"] < float(params[min_elevation_parameter]) ])

        # Delete listed keys from available vertices
        for v in del_keys:
            if v in graph:
                graph.remove_node(v)

        # Process start/end points
        # Check vertices for appropriate inclusion in start and end points
        spts = [ v for v in graph.nodes(data=False) if startpoly.containsPoint(GeoUtils.Features.Point(x=graph.node[v]["latlon"][0],y=graph.node[v]["latlon"][1])) ]
        epts = [ v for v in graph.nodes(data=False) if endpoly.containsPoint(GeoUtils.Features.Point(x=graph.node[v]["latlon"][0],y=graph.node[v]["latlon"][1])) ]

        len_spts = len(spts)
        len_epts = len(epts)
        current_elev = -9999
        best_spt_v = 0
        for v in spts :
            if graph.node[v]["elev"] > current_elev :
                current_elev = graph.node[v]["elev"]
                best_spt_v = v

        current_elev = -9999
        best_ept_v = 0
        for v in epts :
            if graph.node[v]["elev"] > current_elev :
                current_elev = graph.node[v]["elev"]
                best_ept_v = v

        if best_spt_v <> 0 :
            ###print "spts count: %s, pre-selecting %s, elev: %s" % (len_spts,best_spt_v,graph.node[best_spt_v]["elev"])
            spts = [best_spt_v]
        if best_ept_v <> 0 :
            ###print "epts count: %s, pre-selecting %s, elev: %s" % (len_epts,best_ept_v,graph.node[best_ept_v]["elev"])
            epts = [best_ept_v]

        ###print "makeNetworkx, post-delete, pre-graph, final # grid points, after deletions: %s, elapsed time: %.3f" % (graph.number_of_nodes(),time.time()-startMakeNetworkTime,)

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
                    edge_vals = eqns.get(eq)(dist["total"],avg_elev,params)
                    weight = edge_vals['cost']

                    # Add edge to graph if not already there
                    if not graph.has_edge(v,k):
                        graph.add_edge(v,k,weight=weight,vars=edge_vals)

        ###print "makeNetworkx, graph-complete, number of edges: %s, function-complete, elapsed time: %.3f" % (graph.number_of_edges(),time.time()-startMakeNetworkTime,)

    else:
        # Return error message
        errtxt = "Unknown run type selected: [%s].<br/><br/>\n" % (run_type,)

        # Return error text and error
        # Function exits
        return errtxt,True

    # Return graph and no error
    return (grid,old_graph,graph,spts,epts,boundingPoly),False

# Run optimization
# pid - port ID
# w - grid width in degrees (Default: 1)
# h - grid height in degrees (Default: 1)
# eq - design cost equation to use (Default: SUPERSLR Minimum-Criteria Dike Design)
# elevdata - elevation data to use for grid (Default: 30-second SRTM30Plus grid)
def optimize(pid,w,h,eq,elevdata,run_type,current_structure,number_of_buckets=5,bucket_low=-60.0,bucket_high=20.1):
#def optimize(pid,w=1,h=1,eq=GeoUtils.constants.Equations.SMCDD,elevdata=GeoUtils.constants.ElevSrc.DEFAULT30SEC,run_type='networkx',current_structure='dike'):
    '''
    Run Port Protector Optimization

    Parameters
        @param pid - port ID
        @param w - grid width in degrees (default: 1)
        @param h - grid height in degrees (default: 1)
        @param eq - design equation as constant in GeoUtils.constants.Equations (default: SUPERSLR Minimum-Criteria Dike Design)
        @param elevdata - elevation data to use for grid as constant in GeoUtils.constants.ElevSrc (default: 30-second SRTM30Plus)

    '''
    import time
    startOptimizeTime = time.time()
    ###print "optimize %s %s, dataset %s, starting time: %.3f" % (run_type,current_structure,elevdata,startOptimizeTime)
    # Get grid
    response,error = makeNetwork(int(pid),float(w),float(h),eq,elevdata,run_type,current_structure)
    ###print "optimize, post makeNetwork, elapsed time: %.3f" % (time.time()-startOptimizeTime)

    # If there was an error, return error and message
    if error == True:
        errtxt = response
        # Function exits
        return errtxt,True


    from array import array
    # Shortest path details variable holders
    path = []
    pts = []
    elev = []
    length = 0.0
    bucket_size = (bucket_high - bucket_low) / number_of_buckets
    bucket_range = ""
    buckets = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for init_depth in xrange (0, number_of_buckets, 1):
        bucket_range += "%s: [%.2f <= x < %.2f], \n" % ((init_depth + 1), bucket_low + (init_depth * bucket_size), bucket_low + (((init_depth +1) * bucket_size)),)

    tallest_section_depth = -9999.9
    shortest_section_depth = 9999.9

    # Initialize volume variables
    dikeVol = 0.0
    toeVol = 0.0
    coreVol = 0.0
    armorVol = 0.0
    foundVol = 0.0
    totalVol = 0.0

    sand_volume = 0.0
    gravel_volume = 0.0
    quarry_run_stone_volume = 0.0
    large_riprap_volume = 0.0
    small_riprap_volume = 0.0
    concrete_volume = 0.0
    structural_steel_weight = 0.0
    structural_steel_volume = 0.0

    structure_height_above_msl = 0.0

    ###print "optimize, initialized, running %s calculations, elapsed time: %.3f" % (run_type, time.time()-startOptimizeTime)
    if run_type == 'old' :
        # Import shortest path algorithm
        import dijkstra

        # Unpack response
        (grid,old_graph,graph,startpts,endpts,bPoly) = response

        # For each start point and end point
        optimalPaths = [ dijkstra.shortestPath(old_graph,start,end) for end in endpts for start in startpts ]
        ###print "optimize, found %s possible paths, elapsed time: %.3f" % (len(optimalPaths), time.time()-startOptimizeTime)

        # Initialize minimum distance to infinity
        vol = float('inf')
        # Initialize shortest path to false
        sp = False
        # For each path and distance, check to determine if shortest
        for possiblePath in optimalPaths:
            if possiblePath == (False,False):
                pass
            elif float(possiblePath[1]) < vol:
                vol = float(possiblePath[1])
                sp = possiblePath[0]
            else:
                pass
        ###print "optimize, path volumes compared, elapsed time: %.3f" % (time.time()-startOptimizeTime)

        try:
            prev = False
            for v in sp:
                # add up incremental volumes
                if v and prev :
                    dikeVol += old_graph[prev][v]["dikeVol"]
                    toeVol += old_graph[prev][v]["toeVol"]
                    coreVol += old_graph[prev][v]["coreVol"]
                    foundVol += old_graph[prev][v]["foundVol"]
                    armorVol += old_graph[prev][v]["armorVol"]
                    totalVol += old_graph[prev][v]["cost"]


                    sand_volume += old_graph[prev][v]["sand_volume"]
                    gravel_volume += old_graph[prev][v]["gravel_volume"]
                    quarry_run_stone_volume += old_graph[prev][v]["quarry_run_stone_volume"]
                    large_riprap_volume += old_graph[prev][v]["large_riprap_volume"]
                    small_riprap_volume += old_graph[prev][v]["small_riprap_volume"]
                    concrete_volume += old_graph[prev][v]["concrete_volume"]
                    structural_steel_weight += old_graph[prev][v]["structural_steel_weight"]
                    structural_steel_volume += old_graph[prev][v]["structural_steel_volume"]

                    structure_height_above_msl = old_graph[prev][v]["structure_height_above_msl"]

                    current_section_elev = float(old_graph[prev][v]["elev"])
                    current_section_length = float(old_graph[prev][v]["length"])
                    current_section_cost = old_graph[prev][v]["cost"]
                    elev.append(current_section_elev)
                    if current_section_elev > tallest_section_depth :
                        tallest_section_depth = current_section_elev
                    if current_section_elev < shortest_section_depth :
                        shortest_section_depth = current_section_elev
                    current_elev_bucket = int(round((current_section_elev - bucket_low ) * 100.0 / bucket_size)) / 100
                    if not (current_elev_bucket >= number_of_buckets or current_elev_bucket < 0):
                        buckets[current_elev_bucket] += current_section_length
                    ###else :
                        ###print "Warning! section is out of bucketing range, elev:%.2f, length:%.2f, cost:%.2f, attempted bucket:%s" % (current_section_elev,current_section_length,old_graph[prev][v]["cost"],current_elev_bucket + 1,)

                # Add point details to paths
                path.append(grid[v]["latlon"])
                pts.append(grid[v]["metric"])
                elev.append(float(grid[v]["elev"]))

                # Set previous point to current point
                prev = v
            ###print "optimize, optimal path values calculated, elapsed time: %.3f" % (time.time()-startOptimizeTime)
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

    elif run_type == 'networkx' :
        # Import graph handling tools
        import networkx as nx

        # Unpack response
        (grid,old_graph,graph,startpts,endpts,bPoly) = response

        if (len(startpts) < 1 or len(endpts) < 1) :
            # Return error message
            errtxt = "There are no data points in the starting and/or ending polygon.<br/><br/>\n"
            errtxt += "Starting Polygon data point count: %s " % (len(startpts),)
            errtxt += "End Polygon data point count: %s " % (len(endpts),)
            errtxt += "Please update the StartEnd polygons to match the desired data set."
            errtxt += "or report this error to %s " % (GeoUtils.constants.contactEmail,)
            errtxt += "along with the following information:\n"
            errtxt += "Port ID - %s\n" % (pid,)

            # Return error text and error
            # Function exits
            return errtxt,True

        # Dictionary of costs to paths
        SPs = {}

        # Run shortest path algorithm for each start point and end point
        for start in startpts:
            for end in endpts:
                short_path = nx.shortest_path(graph,source=start,target=end,weight="weight")
                vol = 0.0
                for pt in range(0,len(path)-1):
                    vol += graph[short_path[pt]][short_path[pt+1]]['vars']['cost']

                SPs[vol] = short_path
        ###print "optimize, found %s possible paths, elapsed time: %.3f" % (len(SPs), time.time()-startOptimizeTime)

        # Find minimum volume
        minVol = min(SPs.keys())

        # Select shortest path based on minimum volume
        shortestPath = SPs[minVol]
        ###print "optimize, path volumes compared, elapsed time: %.3f" % (time.time()-startOptimizeTime)

        # Calculate piece volumes and path lists
        for pt in range(0,len(shortestPath)):
            if pt > 0:
                dikeVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["dikeVol"]
                toeVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["toeVol"]
                coreVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["coreVol"]
                foundVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["foundVol"]
                armorVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["armorVol"]
                totalVol += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["cost"]

                sand_volume += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["sand_volume"]
                gravel_volume += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["gravel_volume"]
                quarry_run_stone_volume += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["quarry_run_stone_volume"]
                large_riprap_volume += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["large_riprap_volume"]
                small_riprap_volume += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["small_riprap_volume"]
                concrete_volume += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["concrete_volume"]
                structural_steel_weight += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["structural_steel_weight"]
                structural_steel_volume += graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["structural_steel_volume"]

                structure_height_above_msl = graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["structure_height_above_msl"]

                current_section_elev = float(graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["elev"])
                current_section_length = float(graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["length"])
                current_section_cost = float(graph[shortestPath[pt-1]][shortestPath[pt]]["vars"]["cost"])
                elev.append(current_section_elev)

                if current_section_elev > tallest_section_depth :
                    tallest_section_depth = current_section_elev
                if current_section_elev < shortest_section_depth :
                    shortest_section_depth = current_section_elev
                current_elev_bucket = int(round((current_section_elev - bucket_low ) * 100.0 / bucket_size)) / 100
                if not (current_elev_bucket >= number_of_buckets or current_elev_bucket < 0):
                    buckets[current_elev_bucket] += current_section_length
                ###else :
                    ###print "Warning! section is out of bucketing range, elev:%.2f, length:%.2f, cost:%.2f, attempted bucket:%s" % (current_section_elev,current_section_length,current_section_cost,current_elev_bucket + 1,)

            path.append(graph.node[shortestPath[pt]]["latlon"])
            pts.append(graph.node[shortestPath[pt]]["metric"])
            elev.append(float(graph.node[shortestPath[pt]]["elev"]))
        ###print "optimize, optimal path values calculated, elapsed time: %.3f" % (time.time()-startOptimizeTime)


    else:
        # Return error message
        errtxt = "Unknown run type selected: [%s].<br/><br/>\n" % (run_type,)

        # Return error text and error
        # Function exits
        return errtxt,True

    ###print "optimize, ready to show buckets, elapsed time: %.3f" % (time.time()-startOptimizeTime)
    ###print "buckets - number: %s, high: %s, low: %s, size: %s - actual elev range, high:%.2f, low:%.2f" % (number_of_buckets,bucket_high,bucket_low,bucket_size,tallest_section_depth,shortest_section_depth, )
    bucket_values = ""
    for init_depth in xrange (0, number_of_buckets, 1):
        bucket_values += "%s: [%.2f],    \n" % ((init_depth + 1), buckets[init_depth],)
    ###print bucket_range
    ###print bucket_values
    ###print "optimize, buckets displayed, elapsed time: %.3f" % (time.time()-startOptimizeTime)

    # Average elevation along path
    avg_elev = sum(elev) / len(elev)

    # Prepare values used to update database
    output = (path,avg_elev,totalVol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,bucket_high,bucket_low,number_of_buckets,buckets[0],buckets[1],buckets[2],buckets[3],buckets[4],buckets[5],buckets[6],buckets[7],buckets[8],buckets[9],buckets[10],buckets[11],buckets[12],buckets[13],buckets[14],buckets[15],buckets[16],buckets[17],buckets[18],buckets[19],tallest_section_depth,shortest_section_depth)
    ###print "optimize, output prepared, returning, elapsed time: %.3f" % (time.time()-startOptimizeTime)

    # Return output and no error
    return output,False

# Update database
def updateDB(current_structure,run_type,ge_key,pid,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,eq,elevdata,computeCenter,grid_height,grid_width,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth):
    '''
    Update database with simulation result

    Parameters
        @param current_structure - berm or dike
        @param run_type - networkx or old
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
    import time
    startUpdateDBTime = time.time()
    print "updateDB %s %s, dataset %s, starting time: %.3f" % (run_type,current_structure,elevdata,startUpdateDBTime)

    model_table = ''
    history_table = ''
    if current_structure == 'dike' :
        model_table = 'portprotector'
        history_table = 'portprotector_history'
    elif current_structure == 'berm' :
        model_table = 'berm_model'
        history_table = 'berm_model_history'

    # Get current user details
    DBhandle.setConnUserKey(ge_key)
    user = DBhandle.ConnUserName()

    # Delete old model run and insert into history
    selq = 'SELECT portID,timestamp,attribution,avg_elev,path_length,path_volume,dike_volume,core_volume,toe_volume,foundation_volume,armor_volume,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,AsText(path_geometry),3Dfile,equation,elev_data,computeCenter,grid_height,grid_width,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth FROM %s WHERE ' % (model_table,)
    selq += 'portID=%s' % (pid)
    seldata,selrc = DBhandle.query(selq)
    print "updateDB, previous run data selected, elapsed time: %.3f" % (time.time()-startUpdateDBTime)

    for r in seldata:
        histq = "INSERT INTO %s (portID,created,attribution,avg_elev,path_length,path_volume,dike_volume,core_volume,toe_volume,foundation_volume,armor_volume,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,path_geometry,3Dfile,equation,elev_data,computeCenter,grid_height,grid_width,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth) VALUES ('" % (history_table,)
        histq += "%(portID)s','%(timestamp)s','%(attribution)s','%(avg_elev)s','%(path_length)s','%(path_volume)s','%(dike_volume)s','%(core_volume)s','%(toe_volume)s','%(foundation_volume)s','%(armor_volume)s','%(sand_volume)s','%(gravel_volume)s','%(quarry_run_stone_volume)s','%(large_riprap_volume)s','%(small_riprap_volume)s','%(concrete_volume)s','%(structural_steel_weight)s','%(structural_steel_volume)s','%(structure_height_above_msl)s',PolyFromText('%(AsText(path_geometry))s'),'%(3Dfile)s','%(equation)s','%(elev_data)s','%(computeCenter)s','%(grid_height)s','%(grid_width)s','%(bucket_high)s','%(bucket_low)s','%(number_of_buckets)s','%(bucket_count_1)s','%(bucket_count_2)s','%(bucket_count_3)s','%(bucket_count_4)s','%(bucket_count_5)s','%(bucket_count_6)s','%(bucket_count_7)s','%(bucket_count_8)s','%(bucket_count_9)s','%(bucket_count_10)s','%(bucket_count_11)s','%(bucket_count_12)s','%(bucket_count_13)s','%(bucket_count_14)s','%(bucket_count_15)s','%(bucket_count_16)s','%(bucket_count_17)s','%(bucket_count_18)s','%(bucket_count_19)s','%(bucket_count_20)s','%(tallest_section_depth)s','%(shortest_section_depth)s')" % r
        histdata,histrc = DBhandle.query(histq)
    print "updateDB, previous run data archived, elapsed time: %.3f" % (time.time()-startUpdateDBTime)

    delq = 'DELETE FROM %s WHERE portID=%s' % (model_table,pid,)
    deldata,delrc = DBhandle.query(delq)
    print "updateDB, previous run data deleted from primary, elapsed time: %.3f" % (time.time()-startUpdateDBTime)

    # Create path for linestring creation
    ShortestPath = GeoUtils.Features.Path()
    ShortestPath.fromPointList(path)
    print "updateDB, shortestPath run on features, elapsed time: %.3f" % (time.time()-startUpdateDBTime)

    # Insert shortest path and volume into database
    insertq = "INSERT INTO %s (portID,attribution,avg_elev,path_length,path_volume," % (model_table,) +\
            "dike_volume, core_volume, toe_volume, foundation_volume, armor_volume,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl," +\
            "path_geometry,3Dfile,equation,elev_data,computeCenter,grid_height,grid_width,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth) "
    insertq += "VALUES ('%s','%s','%s','%s','%s'," % (pid,user,avg_elev,ShortestPath.length(),vol)
    insertq += "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " % (dikeVol, coreVol, toeVol, foundVol, armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl)
    insertq += "PolyFromText('%s'),'','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (ShortestPath.toMySQL_linestring(),eq,elevdata,computeCenter,grid_height,grid_width,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth)
    insertdata,insertrc = DBhandle.query(insertq)
    print "updateDB, new run inserted into primary, elapsed time: %.3f" % (time.time()-startUpdateDBTime)

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
        portID = qv["PortID"].value
        w = qv["GridWidth"].value
        h = qv["GridHeight"].value
        simulation_equation = qv["Equation"].value
        elevdata = qv["ElevationData"].value
    except KeyError:
        ge_key = '14b9055d351595cc332c92eec2a06ebf'
        portID = 63
        w = .25
        h = .25
        simulation_equation = GeoUtils.constants.Equations.NTC_CS
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
        response_dike,error_dike = optimize(pid=portID,w=w,h=h,eq=simulation_equation,elevdata=elevdata,run_type='networkx',current_structure='dike')
        if error_dike == True:
            # Output error message
            output = GeoUtils.Interface.uniForm.fullErrorMsgGen(response_dike)
            print output
        response_berm,error_berm = optimize(pid=portID,w=w,h=h,eq=simulation_equation,elevdata=elevdata,run_type='networkx',current_structure='berm')
        if error_berm == True:
            # Output error message
            output = GeoUtils.Interface.uniForm.fullErrorMsgGen(response_berm)
            print output

        # Stop clock
        EndTime = time.time()

        # Elapsed time
        ElapsedTime = EndTime - StartTime

        if error_berm != True and error_dike != True :
            # Unpack response from optimization
            path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth = response_dike

            # Update database
            response,error = updateDB('dike','networkx',ge_key,portID,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,simulation_equation,elevdata,GeoUtils.constants.computeCenter(),h,w,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth)

            if error:
                # Output error message
                msg = "<h3>Error:</h3>\n<p>There was an error updating the database for dike calculation. Please try again.</p>"
                output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)
                print output
            else:
                # Output success message
                msg = '<h3>Success:</h3>\n<p>Please refresh your window to view the result.</p>\n'
                msg += '<br/><p>Model runtime: %f seconds</p>\n' % (ElapsedTime,)
                output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)
                print output

            # Unpack response from optimization
            path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth = response_berm

            # Update database
            response,error = updateDB('berm','networkx',ge_key,portID,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,simulation_equation,elevdata,GeoUtils.constants.computeCenter(),h,w,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth)

            if error:
                # Output error message
                msg = "<h3>Error:</h3>\n<p>There was an error updating the database for berm calculation. Please try again.</p>"
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
