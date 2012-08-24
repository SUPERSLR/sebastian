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
    portdata, count = DBhandle.query('SELECT DISTINCT ID,grid_height,grid_width,elev_data FROM portdata')
    
    print 'Ports to update:' + str(count)
    print 
    
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
            # Print status
            print 'Port: %s' % (portID,)
            # Run model
            response,error = portprotector.optimize(portID,h,w,GeoUtils.constants.Equations.BMASW,port['elev_data'])
            # If error, print error message
            if error == True:
                # Output error message
                output = GeoUtils.Interface.uniForm.fullErrorMsgGen(response)
                print output
            else:
                # Unpack response from optimization
                path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol = response
                # Update database
                response,error = portprotector.updateDB('2ee9a2ec7ebffaecc61f8f011981852e',portID,path,avg_elev,length,vol,dikeVol,coreVol,toeVol,foundVol,armorVol,GeoUtils.constants.Equations.BMASW,port['elev_data'],GeoUtils.constants.computeCenter(),h,w)
                # Add entry to portdata as well
                updateq = 'UPDATE portdata SET defense_volume=%s WHERE ID=%s' % (vol,portID)
                response2,error2 = DBhandle.query(updateq)
        except:
            continue

#    print portprotector.optimize(6, '', .25, .25, GeoUtils.constants.Equations.BMASW, GeoUtils.constants.ElevSrc.DEFAULT30SEC)
    print GeoUtils.Interface.StdHTMLFooter()
