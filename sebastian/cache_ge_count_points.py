#!/usr/bin/python

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


def get_points():
    import sys

    port_override = 0
    data_set = 'google_web_service_3sec'

    if len(sys.argv) != 2:
        return 'Usage: python test_ge.py dataset', True
    else :
        data_set = sys.argv[1]

    processing_failover = '1 DAY'
    output = 'output'

    # Select elevation grid size based on elevation data source
    dr = GeoUtils.constants.ElevSize.get(data_set)
    print "dr:%s" % (dr,)
    # Connect to main database
    DBhandle = GeoUtils.RDB()
    DBhandle.connect('uws_ge')

    # Connect to collect database
    collectDBhandle = GeoUtils.RDB()
    collectDBhandle.connect('uws_collect')

    collect_query = "SELECT ID,port_id,status FROM setup_gather_%s where not (status = 'complete' or (status = 'processing' and last_updated > DATE_SUB(now(),INTERVAL %s))) order by process_order" % (data_set,processing_failover,)

    collect_info, collect_count = collectDBhandle.query(collect_query)

    # If not only one port returned from database, raise error
    if collect_count == 0 :
        # Return error
        errtxt = "There are no remaining collections for %s. <br/><br/>\n" % (data_set,)

        # Return error text and error
        # Function exits
        return errtxt,True

    total_point_count = 0

    for port in collect_info :

        port_id = float(port['port_id'])
        port_status = port['status']

        port_query = "SELECT DISTINCT ID, name, latitude, longitude, grid_height, grid_width, elev_data FROM portdata where id in (%s)" % (int(port_id),)
        portdata, portrowcount = DBhandle.query(port_query)

        # If not only one port returned from database, raise error
        if portrowcount == 0 or portrowcount > 1:
            # Return error
            errtxt = "There was an error while retrieving the port data. <br/><br/>\n"
            errtxt += "Please report this error to %s " % (GeoUtils.constants.contactEmail,)
            errtxt += "including the following information: "
            errtxt += "Port ID - %s, Number of ports - %s" % (port_id,portrowcount)

            # Return error text and error
            # Function exits
            return errtxt,True

        # Unpack parameters
        h = portdata[0]['grid_height']
        w = portdata[0]['grid_width']
        portname = portdata[0]['name']
        # Get port latitude and longitude
        port_lat = float(portdata[0]['latitude'])
        port_lon = float(portdata[0]['longitude'])

        shard_table_name = GeoUtils.constants.getShardTable(port_lat,port_lon,data_set)


        totalTime = 0
        portResult = 'success'

        # Import time module to record runtime
        import time

        try:
            if h == 0:
                h = 0.25
            if w == 0:
                w = 0.25

            if portResult == 'failed' :
                print 'Port simulation failed!'
            # Print status
            print 'Port: %s Name: %s' % (port_id,portname, )
            # Run model

            # Start clock
            StartTime = time.time()

            portResult = 'failed'
            ###print 'before optimize'



            #dr = .05
            # Determine bounding box for area of interest surrounding port
            west = float(port_lon) - float(w) / 2
            east = float(port_lon) + float(w) / 2
            north = float(port_lat) + float(h) / 2
            south = float(port_lat) - float(h) / 2

            print "west %s, east %s, north %s, south %s" % (west, east, north, south,)
            #TODO: connect to GE export DB and find last end point, set restarting bool value

            start_lat = west
            start_lng = south

            if port_status == 'incomplete' or port_status == 'processing' :
                # Query database for port details
                startlocationq = "SELECT latitude,longitude FROM %s WHERE port_id='%s' order by latitude asc, longitude asc" % (shard_table_name,port_id,)
                startlocation,startrowcount = collectDBhandle.query(startlocationq)

                if startrowcount > 0 :
                    start_lat = startlocation[0]['latitude']
                    start_lon = startlocation[0]['longitude']

            current_count = 0
            current_lat = start_lat
            current_lng = start_lng
            point_list = list()
            #build array of desired points
            while (current_lat <= east) :
                while (current_lng <= north) :
                    current_count += 1
                    #point_list.append([current_lat, current_lng])
                    current_lng += dr
                current_lng = start_lng
                current_lat += dr

            total_point_count += current_count
            print current_count
            #for point in point_list :
            #    print "%s %s" % (point[0], point[1])


            ###print 'after optimize'
            portResult = 'success'

            # Stop clock
            EndTime = time.time()

            # Elapsed time
            ElapsedTime = EndTime - StartTime
            totalTime += ElapsedTime
            print 'simulation time: %f total: %f' % (ElapsedTime, totalTime, )

        except:
            import sys,traceback
            print 'Unexpected error:<br/><br/>\n<pre>\n%s\n</pre>\n<br/>\n\n' % (traceback.format_exc(),)


    print "dr:%s" % (dr,)
    print "total_point_count: %s" % (total_point_count,)
    # Close database
    DBhandle.close()
    # Close database
    collectDBhandle.close()

    return output,False

# If called directly, run with given query string parameters
if __name__ == "__main__":
    output = 'main empty output'
    try:
        # Import time module to record runtime
        import time

        # Start clock
        StartTime = time.time()

        # Run optimization to obtain shortest path
        response,error = get_points()

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
            print output
    except:
        import sys,traceback
        print 'Unexpected error:<br/><br/>\n<pre>\n%s\n</pre>\n<br/>\n\n' % (traceback.format_exc(),)

    #print GeoUtils.Interface.StdHTMLFooter()

