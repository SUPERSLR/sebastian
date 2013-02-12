#!/usr/bin/python

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


def load_points():
    import sys
    import os
    import time

    load_per_query = 10000

    usage = 'Usage: python %s file_to_load data_source elevation_column_number latitude_column_number longitude_column_number' % (__file__,)
    if len(sys.argv) != 6 :
        return usage, True
    else :
        try :
            file_to_load = sys.argv[1]
            data_source = sys.argv[2]
            elevation_column_number = int(sys.argv[3])
            latitude_column_number = int(sys.argv[4])
            longitude_column_number = int(sys.argv[5])
        except:
            return 'Warning, column numbers must be integers, %s' % (usage), True

    print "file_to_load [%s], data_source [%s], elevation_column_number [%s], latitude_column_number [%s], longitude_column_number [%s]" % (file_to_load, data_source, elevation_column_number, latitude_column_number, longitude_column_number)
    output = ""
    count_lines = 0
    count_loaded = 0

    # Connect to collect database
    loadDBhandle = GeoUtils.RDB()
    loadDBhandle.connect('uws_maps')

    file_in = open(file_to_load, "r")
    line = file_in.readline()

    current_load_count = 0
    load_query_root = "INSERT INTO elev_data_all_%s (elevation, latitude, longitude, source) VALUES " % (data_source)
    load_values = ""
    line_separator = ""
    while line:
        if current_load_count >= load_per_query :
            # save a set of load_per_query load values
            load_query = "%s %s;" % (load_query_root, load_values)
            load_info, load_count = loadDBhandle.query(load_query)
            #print "load_info: %s, load_count: %s" % (load_info, load_count)
            if load_count > 0 :
                count_loaded += load_count
            current_load_count = 0
            load_values = ""
            line_separator = ""

        line_list = line.split(',')
        count_lines += 1
        try :
            elevation = float(line_list[elevation_column_number - 1])
            latitude = float(line_list[latitude_column_number - 1])
            longitude = float(line_list[longitude_column_number - 1])

            load_values += "%s('%s', '%s', '%s', '%s')" % (line_separator, elevation, latitude, longitude, data_source)
            line_separator = ", "
            current_load_count += 1
        except :
            print "line not formatted for importing: [%s] [%s]" % (count_lines, line)

        line = file_in.readline()

    if current_load_count > 0 :
        # save any partial sets of data after completing file read
        load_query = "%s %s;" % (load_query_root, load_values)
        load_info, load_count = loadDBhandle.query(load_query)
        #print "load_info: %s, load_count: %s" % (load_info, load_count)
        if load_count > 0 :
            count_loaded += load_count

    # Close database
    loadDBhandle.close()

    print "%s lines read, %s records loaded, %s lines not formatted for loading" % (count_lines, count_loaded, count_lines-count_loaded)

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
        response,error = load_points()

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
            print "Elapsed time:%.4f seconds" % (ElapsedTime)
    except:
        import sys,traceback
        print 'Unexpected error:<br/><br/>\n<pre>\n%s\n</pre>\n<br/>\n\n' % (traceback.format_exc(),)

    #print GeoUtils.Interface.StdHTMLFooter()

