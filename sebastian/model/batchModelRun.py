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

    #IDs, count = DBhandle.query('SELECT DISTINCT portID FROM portprotector')
    #portdata, count = DBhandle.query('SELECT DISTINCT ID,name,map_region,grid_height,grid_width,elev_data FROM portdata')
    portdata, count = DBhandle.query('SELECT DISTINCT ID,name,map_region,grid_height,grid_width,elev_data FROM portdata where id > 126 and id < 128')

    print 'Ports to update:' + str(count)
    print

    totalTime = 0
    portResult = 'success'

    # Import time module to record runtime
    import time
    import portprotector
    for port in portdata:
        try:
            # Unpack parameters
            h = port['grid_height']
            w = port['grid_width']

            if h == 0:
                h = 0.25
            if w == 0:
                w = 0.25

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
            ###print 'before optimize'
            response,error = portprotector.optimize(portID,h,w,GeoUtils.constants.Equations.KMB2,port['elev_data'],port['map_region'])
#            response,error = portprotector.optimize(portID,h,w,GeoUtils.constants.Equations.BMASW,port['elev_data'])
            ###print 'after optimize'
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
                path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol = response
                # Update database
#22938b6006b66b4eecd09f3b38c8c961 #Keith key development
#                response,error = portprotector.updateDB('2ee9a2ec7ebffaecc61f8f011981852e',portID,path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,GeoUtils.constants.Equations.BMASW,port['elev_data'],GeoUtils.constants.computeCenter(),h,w)
                response,error = portprotector.updateDB('22938b6006b66b4eecd09f3b38c8c961',portID,path,avg_elev,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,GeoUtils.constants.Equations.BMASW,port['elev_data'],GeoUtils.constants.computeCenter(),h,w)
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
