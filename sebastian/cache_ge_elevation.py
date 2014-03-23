#!/usr/bin/python

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


def get_points():
    import sys
    import os
    import time


    max_request_count = 2500
    max_location_count = 25000
    locations_per_request = 1

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

    port_id = float(collect_info[0]['port_id'])
    port_status = collect_info[0]['status']

    port_query = "SELECT DISTINCT ID, name, latitude, longitude, grid_height, grid_width, elev_data FROM portdata where id = %i" % (int(port_id),)
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

        #TODO: connect to GE export DB and find last end point, set restarting bool value

        start_lat = south
        start_lng = west
        print "default start_lat: %s, start_lng: %s" % (start_lat, start_lng, )

        if port_status == 'incomplete' or port_status == 'processing' :
            # Query database for port details
            startlocationq = "SELECT latitude,longitude FROM %s WHERE port_id='%s' order by latitude asc, longitude asc" % (shard_table_name,port_id,)
            startlocation,startrowcount = collectDBhandle.query(startlocationq)

            if startrowcount > 0 :
                start_lat = startlocation[0]['latitude']
                start_lon = startlocation[0]['longitude']

        print "update start_lat: %s, start_lng: %s" % (start_lat, start_lng, )
        current_lat = start_lat
        current_lng = start_lng
        point_list = list()
        #build array of desired points
        while (current_lat <= north) :
            while (current_lng <= east) :
                point_list.append([current_lat, current_lng])
                current_lng += dr
            current_lng = start_lng
            current_lat += dr

        print "Number of points: %s" % (len(point_list),)
        print "Points per request: %s" % (locations_per_request,)
        #for point in point_list :
        #    print "%s %s" % (point[0], point[1])



        print 'testing GE extract'

        request_count = 0
        location_count = 0
        request_count_today = 0
        location_count_today = 0

        # Database query
        table = 'elev_data'
        elev_table_list,error = GeoUtils.constants.getAllShardTables(data_set)
        # If there was an error, return error and message
        if error == True:
                errtxt = elev_table_list
                # Function exits
                return errtxt,True
        union_text = ''
        dbq = ""
        for shard in elev_table_list:
                dbq += union_text
                dbq += "(SELECT count(*) as location_count FROM %s_%s_%s WHERE " % (table,shard,data_set,)
                dbq += " collected >  DATE_SUB(now(),INTERVAL 1 DAY))"
                union_text = " UNION "

        #print dbq
        # Query database
        dbdata,rowcount = collectDBhandle.query(dbq)

        if rowcount > 0:
            location_count_today = 0
            for row in dbdata :
                location_count_today += row['location_count']

        # Database query
        table = 'elev_data'
        elev_table_list,error = GeoUtils.constants.getAllShardTables(data_set)
        # If there was an error, return error and message
        if error == True:
                errtxt = elev_table_list
                # Function exits
                return errtxt,True
        union_text = ''
        dbq = ""
        for shard in elev_table_list:
                dbq += union_text
                dbq += "(SELECT count(distinct(run_id)) as request_count FROM %s_%s_%s WHERE " % (table,shard,data_set,)
                dbq += " collected >  DATE_SUB(now(),INTERVAL 1 DAY))"
                union_text = " UNION "

        #print dbq
        # Query database
        dbdata,rowcount = collectDBhandle.query(dbq)

        if rowcount > 0:
            request_count_today = 0
            for row in dbdata :
                request_count_today += row['request_count']

        request_count = request_count_today
        location_count = location_count_today
        print "starting counts, request: %s location: %s " % (request_count,location_count,)

        #import library to do http requests:
        import urllib
        import urllib2

        #import easy to use xml parser called minidom:
        from xml.dom.minidom import parseString
        #all these imports are standard on most modern python implementations

        current_point = 0
        point_count = len(point_list)
        while (request_count < max_request_count and location_count < max_location_count and current_point < point_count) :

            run_id = "rid%s%s_%s" % (os.getpid(),time.clock(),current_point)
            #print "run_id: %s" % (run_id,)

            request_count += 1
            location_count += min(locations_per_request, point_count - current_point)

            last_request_point = current_point + locations_per_request
            location_list = "%s,%s" % (point_list[current_point][0],point_list[current_point][1],)
            current_point += 1
            while (current_point < last_request_point and current_point < point_count) :
                location_list = "%s|%s,%s" % (location_list,point_list[current_point][0],point_list[current_point][1],)
                current_point += 1

            #print location_list
            url = "http://maps.googleapis.com/maps/api/elevation/xml"
            values = {'sensor':'false','locations':location_list}
            data = urllib.urlencode(values)

            get_url = "%s?locations=%s&sensor=false" % (url,location_list,)

            #download the file:
            #file = urllib2.urlopen('http://maps.googleapis.com/maps/api/elevation/xml?locations=39.7391536,-104.9847034|36.455556,-116.866667&sensor=false')
            #file = urllib2.urlopen('http://local.seaports2100.org/sebastian/test_ge.xml', data)
            file = urllib2.urlopen(get_url)
            #file = urllib2.urlopen(url,data)
            #file = urllib2.urlopen(url,values)
            #print get_url;

            #convert to string:
            data = file.read()

            #close file because we dont need it anymore:
            file.close()
            #parse the xml you downloaded
            dom = parseString(data)
            #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
            statusTag = dom.getElementsByTagName('status')[0].toxml()
            #strip off the tag (<tag>data</tag>  --->   data):
            statusData=statusTag.replace('<status>','').replace('</status>','')

            #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
            resultTags = dom.getElementsByTagName('result')
            #print resultTags[0].toxml()
            for result in resultTags:
                latData = result.getElementsByTagName('lat')[0].firstChild.nodeValue
                #print "lat: %s" % (latData, )
                lngData = result.getElementsByTagName('lng')[0].firstChild.nodeValue
                #print "lng: %s" % (lngData, )
                elevData = result.getElementsByTagName('elevation')[0].firstChild.nodeValue
                #print "elev: %s" % (elevData, )
                resData = result.getElementsByTagName('resolution')[0].firstChild.nodeValue
                #print "resolution: %s" % (resData, )

                collect_query = "INSERT INTO %s_%s_%s (run_id,status,port_id,latitude,longitude,elevation,resolution,source) " % (table,shard,data_set,)
                collect_query += "VALUES ('%s', 'complete','%s', '%s', '%s', '%s', '%s', '%s')" % (run_id,port_id,latData,lngData,elevData,resData,data_set,)
                collect_info, collect_count = collectDBhandle.query(collect_query)

            #print "query result: %s | %s" % (collect_info, collect_count,)



        ###print 'after optimize'
        portResult = 'success'
        print "request_count: %s  location_count: %s" % (request_count, location_count, )

        # Stop clock
        EndTime = time.time()

        # Elapsed time
        ElapsedTime = EndTime - StartTime
        totalTime += ElapsedTime
        print 'simulation time: %f total: %f' % (ElapsedTime, totalTime, )

    except:
        import sys,traceback
        print 'Unexpected error:<br/><br/>\n<pre>\n%s\n</pre>\n<br/>\n\n' % (traceback.format_exc(),)


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

