#!/usr/bin/python
# Ben Pedrick
# A script to run every port with the BMASW design

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath('../'))
    import GeoUtils

    print GeoUtils.Interface.ContentType('html')
    print

    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())

    DBhandle = GeoUtils.RDB()
    DBhandle.connect('uws_ge')

    run_type = ''
    dataset_override = ""
    h_override = ""
    w_override = ""
    #dataset_override = GeoUtils.constants.ElevSrc.GOOGLE3SEC
    #dataset_override = GeoUtils.constants.ElevSrc.NOAAASTER30M
    dataset_override = GeoUtils.constants.ElevSrc.DEFAULT30SEC
    #h_override = 0.20
    #w_override = 0.17
    run_type = 'networkx'

    simulation_equation = GeoUtils.constants.Equations.KDBS
    #simulation_equation = GeoUtils.constants.Equations.KMB2
    #simulation_equation = GeoUtils.constants.Equations.BMASW

    if len(sys.argv) > 1 :
        port_number = int(sys.argv[1])
        portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = %s' % (port_number))
        if len(sys.argv) > 2 and sys.argv[2] == 'x' :
            run_type = 'networkx'
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

        #all US10 at once
        portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 112 or id = 114 or id = 116 or id = 117 or id = 125 or id = 127 or id = 131 or id = 135 or id = 141 or id = 180 order by id desc')

        #all US10 one at a time

        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 112 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 114 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 116 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 117 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 125 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 127 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 131 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 135 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 141 ')
        #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 180')

    print 'Ports dikes to update:' + str(count)
    print

    totalTime = 0
    portResult = 'success'

    # Import time module to record runtime
    import time
    import portprotector
    import dike_model_networkx
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

            #print 'w'
            #print w
            #print 'h'
            #print h


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
                response,error = dike_model_networkx.optimize(portID,h,w,simulation_equation,dataset)
            else :
                response,error = portprotector.optimize(portID,h,w,simulation_equation,dataset)
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
                path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl = response

                # Update database
#22938b6006b66b4eecd09f3b38c8c961 #Keith key development
            if run_type == 'networkx' :
                response,error = dike_model_networkx.updateDB('22938b6006b66b4eecd09f3b38c8c961',portID,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,simulation_equation,dataset,GeoUtils.constants.computeCenter(),h,w)
            else :
                response,error = portprotector.updateDB('22938b6006b66b4eecd09f3b38c8c961',portID,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,sand_volume,gravel_volume,quarry_run_stone_volume,large_riprap_volume,small_riprap_volume,concrete_volume,structural_steel_weight,structural_steel_volume,structure_height_above_msl,simulation_equation,dataset,GeoUtils.constants.computeCenter(),h,w)
                print "portID: %s" % (portID,)
                #print "attribution: %s" % ("Keith Mosher",)
                print "equation: %s" % (simulation_equation,)
                print "elev_data: %s" % (dataset,)
                print "avg_elev: %s" % (avg_elev,)
                print "structure_height_above_msl: %s" % (structure_height_above_msl,)

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
                print "batchModelRun port updates complete"
        except:
            import sys,traceback
            print 'Unexpected error:<br/><br/>\n<pre>\n%s\n</pre>\n<br/>\n\n' % (traceback.format_exc(),)
            continue

    print GeoUtils.Interface.StdHTMLFooter()
