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
    #dataset_override = GeoUtils.constants.ElevSrc.DEFAULT30SEC
    #h_override = 0.20
    #w_override = 0.17
    #run_type = 'networkx'

    simulation_equation = GeoUtils.constants.Equations.KDBS
    #simulation_equation = GeoUtils.constants.Equations.KMB2
    #simulation_equation = GeoUtils.constants.Equations.BMASW
    #simulation_equation = GeoUtils.constants.Equations.SMCDD

    #Args are (in order) dike/berm/both old/x [optional] port number
    if len(sys.argv) < 3 or len(sys.argv) > 4 or not (sys.argv[1] == 'both' or sys.argv[1] == 'dike' or sys.argv[1] == 'berm') :
#or (len(sys.argv) == 4 and not (sys.argv[3] == '10report' or isinstance(sys.argv[3],int)))

        print "usage: batchAllRun.py dike/berm/both old/x port_number/10report[optional]"
        print "Parameter 1: \"dike\" runs just dike calculations, \"berm\" just berm calculations, and \"both\", unsurprisingly, runs both (all dike followed by all berm)."
        print "Parameter 2: This specifies which calculation model to use.  \"x\" uses networkx, which is faster and better, but may not be installed on some machines.  \"old\" uses the original manually entered functions."
        print "Parameter 3: If this is a number, the simulation will be used for a single port of that number.  \"10report\" will run it for the selected 10 ports for the first paper.  If empty all ports will run."
        exit()
    else :
        if sys.argv[2] == 'x' :
            run_type = 'networkx'
            print "run type networkx calculations"
        else :
            print "run type old calculations"
        calc_to_run = sys.argv[1]

    q_base_front = 'SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM '

    if len(sys.argv) == 4 :
        if sys.argv[3] == '10report' :
            #all US10 one at a time
            print "10 report ports: 112, 114, 116, 117, 125, 127, 131, 135, 141, 180"
            q_base_back = ' where id = 112 or id = 114 or id = 116 or id = 117 or id = 125 or id = 127 or id = 131 or id = 135 or id = 141 or id = 180 order by id desc'
            q_ports = q_base_front + port_table + q_base_back
        else :
            port_number = int(sys.argv[3])
            print "port_number %s" % (port_number, )
            q_base_back = ' where id = %s' % (port_number, )
            q_ports = q_base_front + port_table + q_base_back
    elif len(sys.argv) == 3 :
        print "all ports"
        q_ports = q_base_front + port_table
    else :
        #IDs, count = DBhandle.query('SELECT DISTINCT portID FROM portprotector')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id > 113 and id < 115')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 112 or id = 116 or id = 117 or id = 125 or id = 135')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 125')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 117 or id = 141 or id = 180')

        #location problems
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 112')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 117')


        #polygon problems
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 116')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 125')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 135')


        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 112 or id = 114 or id = 116 or id = 117 or id = 125 or id = 127 or id = 131 or id = 135 or id = 141 or id = 180 order by id desc')
        #all US10 one at a time

        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 112 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 114 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 116 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 117 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 125 ')
        portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 127 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 131 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 135 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 141 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 180')


    if calc_to_run == 'both' or calc_to_run == 'dike' :
        portdata_dike, count_dike = DBhandle.query(q_ports)
    if calc_to_run == 'both' or calc_to_run == 'berm' :
        portdata_berm, count_berm = DBhandle.query(q_ports)

    print 'Port dikes to update:' + str(count_dike)
    print
    print 'Port berms to update:' + str(count_berm)
    print

    exit()

    totalTime = 0
    portResult = 'success'

    # Import time module to record runtime
    import time
    import berm_model
    import berm_model_networkx
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
                print 'Port simulation failed!'
            # Print status
            print 'Port: %s Name: %s' % (portID,portname, )
            # Run model

            # Start clock
            StartTime = time.time()

            portResult = 'failed'
            if run_type == 'networkx' :
                response,error = berm_model_networkx.optimize(portID,h,w,simulation_equation,dataset)
            else :
                response,error = berm_model.optimize(portID,h,w,simulation_equation,dataset)
            portResult = 'success'

            # Stop clock
            EndTime = time.time()

            # Elapsed time
            ElapsedTime = EndTime - StartTime
            totalTime += ElapsedTime
            print 'simulation time: %f total: %f' % (ElapsedTime, totalTime, )

            # If error, print error message
            if error == True:
                # Output error message
                print 'Error'
                output = GeoUtils.Interface.uniForm.fullErrorMsgGen(response)
                print output
            else:
                # Unpack response from optimization
                print 'Success'
###                print response
#                path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol = response
                path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume = response

                # Update database
#22938b6006b66b4eecd09f3b38c8c961 #Keith key development
                response,error = berm_model.updateDB('22938b6006b66b4eecd09f3b38c8c961',portID,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,simulation_equation,dataset,GeoUtils.constants.computeCenter(),h,w)
                print "portID: %s" % (portID,)
                #print "attribution: %s" % ("Keith Mosher",)
                print "equation: %s" % (simulation_equation,)
                print "elev_data: %s" % (dataset,)
                print "avg_elev: %s" % (avg_elev,)
                # Create path for linestring creation
                ShortestPath = GeoUtils.Features.Path()
                ShortestPath.fromPointList(path)
                print "path_length: %s" % (ShortestPath.length(),)
                print "path_volume: %s" % (vol,)
                #print "dike_volume: %s" % (dikeVol,)
                #print "core_volume: %s" % (coreVol,)
                #print "toe_volume: %s" % (toeVol,)
                #print "foundation_volume: %s" % (foundVol,)
                #print "armor_volume: %s" % (armorVol,)
                print "computeCenter: %s" % (GeoUtils.constants.computeCenter(),)
                #print "grid_height: %s" % (h,)
                #print "grid_width: %s" % (w,)

                ###print error
                if error == True:
                    # Output error message
                    output = GeoUtils.Interface.uniForm.fullErrorMsgGen(response)
                    print output

                # Add entry to portdata as well
                updateq = 'UPDATE portdata SET defense_volume=%s WHERE ID=%s' % (vol,portID)
                response2,error2 = DBhandle.query(updateq)
        except:
            import sys,traceback
            print 'Unexpected error:<br/><br/>\n<pre>\n%s\n</pre>\n<br/>\n\n' % (traceback.format_exc(),)
            continue

