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

    dataset_override = ""
    h_override = ""
    w_override = ""
    #dataset_override = GeoUtils.constants.ElevSrc.GOOGLE30SEC
    #dataset_override = GeoUtils.constants.ElevSrc.GOOGLEP3SEC
    dataset_override = GeoUtils.constants.ElevSrc.NOAAASTER30M
    #h_override = 0.15
    #w_override = 0.09

    #simulation_equation = GeoUtils.constants.Equations.KMB2
    simulation_equation = GeoUtils.constants.Equations.BMASW

    #IDs, count = DBhandle.query('SELECT DISTINCT portID FROM portprotector')
    #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata')
    #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 112 or id = 114 or id = 116 or id = 117 or id = 125 or id = 127 or id = 131 or id = 135 or id = 141 or id = 180')
    #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 114')
    portdata, count = DBhandle.query('SELECT DISTINCT ID,name,grid_height,grid_width,elev_data FROM portdata where id = 117 or id = 141 or id = 180')

    print 'Ports to update:' + str(count)
    print

    totalTime = 0
    portResult = 'success'

    # Import time module to record runtime
    import time
    import portprotector
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

            #h = port['grid_height']
            #w = port['grid_width']

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
###                print response
#                path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol = response
                path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight = response
                # Update database
#22938b6006b66b4eecd09f3b38c8c961 #Keith key development
#                response,error = portprotector.updateDB('2ee9a2ec7ebffaecc61f8f011981852e',portID,path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,GeoUtils.constants.Equations.BMASW,port['elev_data'],GeoUtils.constants.computeCenter(),h,w)
                response,error = portprotector.updateDB('22938b6006b66b4eecd09f3b38c8c961',portID,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,riprap_volume,aggregate_volume,rebar_volume,cement_volume,riprap_weight,aggregate_weight,rebar_weight,cement_weight,simulation_equation,dataset,GeoUtils.constants.computeCenter(),h,w)
                print "portID: %s" % (portID,)
                print "attribution: %s" % ("Keith Mosher",)
                print "equation: %s" % (simulation_equation,)
                print "elev_data: %s" % (dataset,)
                print "avg_elev: %s" % (avg_elev,)
                # Create path for linestring creation
                ShortestPath = GeoUtils.Features.Path()
                ShortestPath.fromPointList(path)
                print "path_length: %s" % (ShortestPath.length(),)
                print "path_volume: %s" % (vol,)
                print "dike_volume: %s" % (dikeVol,)
                print "core_volume: %s" % (coreVol,)
                print "toe_volume: %s" % (toeVol,)
                print "foundation_volume: %s" % (foundVol,)
                print "armor_volume: %s" % (armorVol,)
                print "computeCenter: %s" % (GeoUtils.constants.computeCenter(),)
                print "grid_height: %s" % (h,)
                print "grid_width: %s" % (w,)
#                print portprotector.updateDB('2ee9a2ec7ebffaecc61f8f011981852e',portID,path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,GeoUtils.constants.Equations.BMASW,port['elev_data'],GeoUtils.constants.computeCenter(),h,w)
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

#    print portprotector.optimize(6, '', .25, .25, GeoUtils.constants.Equations.BMASW, GeoUtils.constants.ElevSrc.DEFAULT30SEC)
    print GeoUtils.Interface.StdHTMLFooter()
