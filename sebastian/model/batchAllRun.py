#!/usr/bin/python
# Keith Mosher
# A script to run port dike and berm calculations

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath('../'))
    import GeoUtils

    DBhandle = GeoUtils.RDB()
    DBhandle.connect('uws_ge')

    run_type = ''
    dataset_override = ""
    h_override = ""
    w_override = ""

    calc_to_run = ''

    number_of_buckets = 5
    bucket_low = -60
    bucket_high = 20.1

    # Query building parameters
    port_table = 'portdata'
    q_dike = ''
    q_berm = ''
    q_base_front = ''
    q_base_back = ''
    portdata_dike = ''
    portdata_berm = ''
    count_dike = 0
    count_berm = 0


    #dataset_override = GeoUtils.constants.ElevSrc.GOOGLE3SEC
    #dataset_override = GeoUtils.constants.ElevSrc.NOAAASTER30M
    dataset_override = GeoUtils.constants.ElevSrc.DEFAULT30SEC
    #dataset_override = GeoUtils.constants.ElevSrc.USGS
    #h_override = 0.50
    #w_override = 0.50
    h_override = 0.40
    w_override = 0.40
    #run_type = 'networkx'

    simulation_equation = GeoUtils.constants.Equations.KDBS
    #simulation_equation = GeoUtils.constants.Equations.KMB2
    #simulation_equation = GeoUtils.constants.Equations.WBMAS
    #simulation_equation = GeoUtils.constants.Equations.SMCDD

    #Args are (in order) dike/berm/both old/x [optional] port number
    if len(sys.argv) < 3 or len(sys.argv) > 7 or not (sys.argv[1] == 'both' or sys.argv[1] == 'dike' or sys.argv[1] == 'berm') :
#or (len(sys.argv) == 4 and not (sys.argv[3] == '10report' or isinstance(sys.argv[3],int)))

        print "usage: batchAllRun.py dike/berm/both old/x port_number/10report[optional] number_of_buckets[optional int] bucket_high[optional float] bucket_low[optional float]"

        print "Parameter 1: \"dike\" runs just dike calculations, \"berm\" just berm calculations, and \"both\",\n unsurprisingly, runs both (all dike followed by all berm)."
        print "Parameter 2: This specifies which calculation model to use.  \"x\" uses networkx, which is faster\n and better, but may not be installed on some machines.  \"old\" uses the original manually entered functions."
        print "Parameter 3: If this is a number, the simulation will be used for a single port of that number.\n  \"10report\" will run it for the selected 10 ports for the first paper.  If \"all\" or empty all ports will run."
        print "Parameter 4: Optional (default 5), integer, the number of buckets (1-20) to use."
        print "Parameter 5: Optional (default -60.0), float, the lowest elevation to bucket from."
        print "Parameter 6: Optional (default 20.1), float, this elev and higher will not be bucketed."
        exit()
    else :
        if sys.argv[2] == 'x' :
            run_type = 'networkx'
            print "run type networkx calculations"
        else :
            run_type = 'old'
            print "run type old calculations"
        calc_to_run = sys.argv[1]

    q_base_front = 'SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM '

    if len(sys.argv) >= 4 :
        if sys.argv[3] == '10report' :
            #all US10 one at a time
            print "10 report ports: 112, 114, 116, 117, 125, 127, 131, 135, 141, 180"
            q_base_back = ' where id = 112 or id = 114 or id = 116 or id = 117 or id = 125 or id = 127 or id = 131 or id = 135 or id = 141 or id = 180 order by id desc'
            q_ports = q_base_front + port_table + q_base_back
        elif sys.argv[3] == 'all' :
            print "all ports"
            q_ports = q_base_front + port_table
        else :
            port_number = int(sys.argv[3])
            print "port_number %s" % (port_number, )
            q_base_back = ' where id = %s' % (port_number, )
            q_ports = q_base_front + port_table + q_base_back
        if len(sys.argv) >= 5 :
            number_of_buckets = int(sys.argv[4])
        if len(sys.argv) >= 6 :
            bucket_low = float(sys.argv[5])
        if len(sys.argv) == 7 :
            bucket_high = float(sys.argv[6])

    elif len(sys.argv) == 3 :
        print "all ports"
        q_ports = q_base_front + port_table


    if calc_to_run == 'both' or calc_to_run == 'dike' :
        portdata_dike, count_dike = DBhandle.query(q_ports)
    if calc_to_run == 'both' or calc_to_run == 'berm' :
        portdata_berm, count_berm = DBhandle.query(q_ports)

    print 'Port dikes to update:' + str(count_dike)
    print
    print 'Port berms to update:' + str(count_berm)
    print

    total_time = 0
    portResult = 'success'
    current_structure = 'dike'

    # Import time module to record runtime
    import time
    import portprotector

    for portdata in [portdata_dike, portdata_berm] :
        for port in portdata:
            try:
                h = 0
                w = 0
                # Unpack parameters
                if h_override == "":
                    h = port['grid_height']
                else :
                    h = h_override

                if w_override == "":
                    w = port['grid_width']
                else :
                    w = w_override


                if h == 0:
                    h = 0.25
                if w == 0:
                    w = 0.25

                if dataset_override == "":
                    dataset = port['elev_data']
                else :
                    dataset = dataset_override

                portID = port['ID']
                portname = port['name']
                if portResult == 'failed' :
                    print 'Port %s %s simulation failed!' % (run_type,current_structure, )
                # Print status
                print 'Port: %s Name: %s' % (portID,portname, )
                # Run model

                # Start clock
                start_time = time.time()

                portResult = 'failed'
                response,error = portprotector.optimize(portID,w,h,simulation_equation,dataset,run_type,current_structure,number_of_buckets,bucket_low,bucket_high)
                portResult = 'success'

                # Stop clock
                end_time = time.time()

                # Elapsed time
                elapsed_time = end_time - start_time
                total_time += elapsed_time
                print '%s %s simulation time: %f total: %f' % (current_structure, run_type, elapsed_time, total_time, )

                # If error, print error message
                if error == True:
                    # Output error message
                    print 'Error'
                    output = GeoUtils.Interface.uniForm.fullErrorMsgGen(response)
                    print output
                else:
                    # Unpack response from optimization
                    print 'Success'
                    path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth = response

                    # Update database
                    #22938b6006b66b4eecd09f3b38c8c961 #Keith key development
                    response,error = portprotector.updateDB(current_structure,run_type,'22938b6006b66b4eecd09f3b38c8c961',portID,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,simulation_equation,dataset,GeoUtils.constants.computeCenter(),h,w,bucket_high,bucket_low,number_of_buckets,bucket_count_1,bucket_count_2,bucket_count_3,bucket_count_4,bucket_count_5,bucket_count_6,bucket_count_7,bucket_count_8,bucket_count_9,bucket_count_10,bucket_count_11,bucket_count_12,bucket_count_13,bucket_count_14,bucket_count_15,bucket_count_16,bucket_count_17,bucket_count_18,bucket_count_19,bucket_count_20,tallest_section_depth,shortest_section_depth)

                    #print "attribution: %s" % ("Keith Mosher",)
                    print "equation: %s" % (simulation_equation,)
                    print "portid (again): %s" % (portID,)
                    print "structure_height_above_msl: %s" % (structure_height_above_msl,)
                    print "avg_elev: %s" % (avg_elev,)
                    print "tallest_section_depth: %s" % (tallest_section_depth,)
                    print "shortest_section_depth: %s" % (shortest_section_depth,)

                    # Create path for linestring creation
                    ShortestPath = GeoUtils.Features.Path()
                    ShortestPath.fromPointList(path)
                    print "path_length: %s" % (ShortestPath.length(),)
                    print "path_volume: %s" % (vol,)
                    print "computeCenter: %s\n\n" % (GeoUtils.constants.computeCenter(),)

                    ###print error
                    if error == True:
                        # Output error message
                        output = GeoUtils.Interface.uniForm.fullErrorMsgGen(response)
                        print output

                    # Add entry to portdata as well
                    if current_structure == 'dike' or calc_to_run != 'both' :
                        updateq = 'UPDATE portdata SET defense_volume=%s WHERE ID=%s' % (vol,portID)
                        response2,error2 = DBhandle.query(updateq)
                    elif current_structure == 'berm' :
                        updateq = 'UPDATE portdata SET defense_volume=defense_volume + %s WHERE ID=%s' % (vol,portID)
                        response2,error2 = DBhandle.query(updateq)
            except:
                import sys,traceback
                print 'Unexpected error:<br/><br/>\n<pre>\n%s\n</pre>\n<br/>\n\n' % (traceback.format_exc(),)
                continue

        current_structure = 'berm'

