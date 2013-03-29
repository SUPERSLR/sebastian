#!/usr/bin/python
# David Newell
# sebastian/savedata/update.py
# Handle and save updated data

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')


# Handle data
# db - dictionary of database information (Format: {'database' : 'value' , 'query' : 'value'}
# fields - data dictionary with field information
# qv - query string values (from form)
# type - item type
# ge_key - user identification key
def handleData(updateFunc,db,fields,qv,type,ge_key=""):
    # Dictionary of functions to generate form field
    fieldRetr = {
            'text' : GeoUtils.Interface.uniForm.textRetr,
            'textarea' : GeoUtils.Interface.uniForm.textareaRetr,
            'radio' : GeoUtils.Interface.uniForm.radioRetr,
            'select' : GeoUtils.Interface.uniForm.selectRetr,
            'hidden' : GeoUtils.Interface.uniForm.hiddenRetr
        }

    # Get user name associated with given key
    DBhandle.setConnUserKey(ge_key)
    user = DBhandle.ConnUserName()


    if 'ID' in qv:
        id = qv['ID'].value
    elif 'PortID' in qv:
        id = qv['PortID'].value
    else:
        id = '0'

    # Query database
    dbdata,drc = DBhandle.query(db['query'] + str(id) + '"')

    # If more than one row or no rows returned, raise error
    if drc > 1 or drc == 0:
        # Return error
        error = "%s database rows returned from edit history." % (drc)

        # Build error message
        msg = '<h3>There was an error while processing your request, please try again later.</h3>\n'
        msg += '<p>If you believe you have received this message in error, please ensure you have correctly downloaded your access file correctly.</p>\n'
        msg += '<p>For all other questions or comments, please contact us (%s), including the information below.</p>\n' % (GeoUtils.constants.contactEmail,)
        msg += '<p><em>%s</em></p>\n' % (error,)

        # Output ok message
        output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)

        # Return output
        # Function exits
        return output

    # Record is first (only) row of data
    r = dbdata[0]

    # Dictionary of form values
    form = {}

    # Convert form names to database keys
    for d in qv:
        for k,v in fields.iteritems():
            if d in v:
                fType = str(v[d][0])
                fOpt = v[d][2]
                fDB = v[d][3]
                form[fDB] = fieldRetr.get(fType)(qv[d],fOpt)

    update = updateFunc(db,id,user,type,r,form)

    return update


# Update Port Characteristics
def updatePortChar(db,id,user,type,d,f):
    # Dictionary of differences
    diff = {}

    # If user note being updated, set Author to current User
    if type == "UserNote":
        f['attribution'] = user

    # Build ok message for later use
    msg = '<h3>Success:</h3>\n<p>Your update is complete! Thanks for your entry.</p>\n'

    # Determine differences and add old and new values to differences dictionary
    for k in d:
        if k == 'AsText(feature_geometry)' and 'feature_geometry' in f:
            pt = GeoUtils.Features.Point()
            pt.fromKML(f['feature_geometry'])
            f[k] = pt.toMySQL_point()
            del f['feature_geometry']
        if not k in f:
            continue
        elif str(d[k]) == str(f[k]):
            continue
        else:
            diff[k] = dict(old=d[k],new=f[k])

    if len(diff) == 0:
        # no changes
        return GeoUtils.Interface.uniForm.fullOkMsgGen(msg)

    # Start update database query
    updateq = 'UPDATE %s SET ' % (db['table'],)

    # Start edit history query list
    editQueries = []

    for k,v in diff.iteritems():
        if k == 'AsText(feature_geometry)':
            updateq += 'feature_geometry=GeomFromText("%s"), ' % (v['new'],)
            v = dict(old='Old Geometry',new='New Geometry')
        else:
            updateq += str(k) + '="%s", ' % (v['new'],)

        editq = 'INSERT INTO edit_history (itemID,type,field,attribution,oldValue,newValue) VALUES '
        editq += '("%s","%s","%s","%s","%s","%s")' % (id,type,k,user,v['old'],v['new'])
        editQueries.append(editq)

    # Strip last comma and space
    updateq = updateq[:-2]

    # Finish update database query
    updateq += ' WHERE ID="%s"' % (id,)

    # Update database
    updatedata,updaterc = DBhandle.query(updateq)

    # Add edits to edit history
    for q in editQueries:
        ed,erc = DBhandle.query(q)

    # Output ok message
    output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)

    # Return output
    return output


# Update Port Polygon
def updatePortPoly(db,id,user,type,d,f):
    # Skip new entry because of no geometry update
    if not 'feature_geometry' in f:
        # If no geometry update, run updatePortChar for new polygon data
        updatePortChar(db,id,user,type,d,f)

        # Build ok message
        msg = '<h3>Success:</h3>\n<p>Your update is complete! Thanks for your entry.</p>\n'

        # Output ok message
        output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)

        # Return output
        return output

    # Define polygon holder variable
    poly = None

    # Convert KML to MySQL geometries
    for k in d:
        if k == 'AsText(feature_geometry)':
            poly = GeoUtils.Features.Polygon()
            poly.fromKML(f['feature_geometry'])
            f[k] = poly.toMySQL_polygon()

    # Polygon area
    if poly == None:
        if 'feature_area' in f:
            polyArea = f['feature_area']
        else:
            polyArea = "-9999"
        if 'feature_perimeter' in f:
            polyPerimeter = f['feature_perimeter']
        else:
            polyPerimeter = "-9999"
    else:
        polyArea = poly.area()
        polyPerimeter = poly.perimeter()

    # Start update database query
    updateq = 'INSERT INTO %s (portID,attribution,feature_type,feature_geometry,feature_area,feature_perimeter) ' % (db['table'],)
    updateq += 'VALUES ("%s","%s","%s",GeomFromText("%s"),"%s","%s")' % (f['portID'],user,f['feature_type'],f['AsText(feature_geometry)'],polyArea,polyPerimeter)

    # Start delete database query
    delq = 'DELETE FROM %s WHERE ID="%s"' % (db['table'],id)

    # Start historical feature query
    histq = 'INSERT INTO historical_features (portID,created,attribution,feature_type,feature_geometry,feature_area,feature_perimeter) '
    if 'feature_perimeter' in d:
        histq += 'VALUES ("%(portID)s","%(timestamp)s","%(attribution)s","%(feature_type)s",GeomFromText("%(AsText(feature_geometry))s"),"%(feature_area)s","%(feature_perimeter)s")' % d
    else:
        histq += 'VALUES ("%(portID)s","%(timestamp)s","%(attribution)s","%(feature_type)s",GeomFromText("%(AsText(feature_geometry))s"),"%(feature_area)s","")' % d

    # Start edit history query
    editq = 'INSERT INTO edit_history (itemID,type,field,attribution,oldValue,newValue) VALUES '
    editq += '("%s","%s","feature_geometry","%s","Old Geometry","New Geometry")' % (id,type,user)

    # Update database with new entry
    ud,urc = DBhandle.query(updateq)
    # Delete old entry
    deld,delrc = DBhandle.query(delq)
    # Insert historical feature into history
    hd,hrc = DBhandle.query(histq)
    # Insert edit history
    ed,erc = DBhandle.query(editq)

    # Build ok message
    msg = '<h3>Success:</h3>\n<p>Your update is complete! Thanks for your entry.</p>\n'
    # Output ok message
    output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)
    # Return output
    return output




# If file called directly, output html
if __name__ == "__main__":
    # Retrieve user information
    qv = []

    # Retrieve post data
    try:
        import cgi
        qv = cgi.FieldStorage()

        try:
            type = str(qv["itemType"].value)
            ge_key = str(qv["GE_KEY"].value)
            error = 'None'
        except KeyError:
            type = 'error'
            ge_key = ''
            error = KeyError
    except:
        type = 'error'
        ge_key = ''
        error = 'Error'


    dbTables = {
            "PortChar" : 'portdata',
            "PortInfraPoly" : 'current_features',
            "BasinPoly" : 'current_features',
            "AvoidPoly" : 'current_features',
            "BermAvoidPoly" : 'current_features',
            "StartEndPoly" : 'current_features',
            "PortPoly" : 'current_features',
            "Country" : 'countries',
            "UserNote" : 'notes',
            "error" : ''
        }

    formFields = {
            "PortChar" : GeoUtils.data.FormDicts.PortChar,
            "PortInfraPoly" : GeoUtils.data.FormDicts.PortPoly,
            "BasinPoly" : GeoUtils.data.FormDicts.PortPoly,
            "AvoidPoly" : GeoUtils.data.FormDicts.PortPoly,
            "BermAvoidPoly" : GeoUtils.data.FormDicts.PortPoly,
            "StartEndPoly" : GeoUtils.data.FormDicts.PortPoly,
            "PortPoly" : GeoUtils.data.FormDicts.PortPoly,
            "Country" : GeoUtils.data.FormDicts.Country,
            "UserNote" : GeoUtils.data.FormDicts.UserNote,
            "error" : ''
        }

    # Dictionary specifying ID field according to item type
    IDfield = {
            "PortChar" : 'PortID',
            "PortInfraPoly" : 'ID',
            "BasinPoly" : 'ID',
            "AvoidPoly" : 'ID',
            "BermAvoidPoly" : 'ID',
            "StartEndPoly" : 'ID',
            "PortPoly" : 'ID',
            "Country" : 'ID',
            "UserNote" : 'ID',
            "error" : ''
        }

    dbqs = {
            "PortChar" : 'SELECT * FROM %s WHERE ID="' % (dbTables.get(type),),
            "PortInfraPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details,feature_area FROM %s WHERE ID="' % (dbTables.get(type),),
            "BasinPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details,feature_area FROM %s WHERE ID="' % (dbTables.get(type),),
            "AvoidPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details,feature_area FROM %s WHERE ID="' % (dbTables.get(type),),
            "BermAvoidPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details,feature_area FROM %s WHERE ID="' % (dbTables.get(type),),
            "StartEndPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details,feature_area FROM %s WHERE ID="' % (dbTables.get(type),),
            "PortPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details,feature_area FROM %s WHERE ID="' % (dbTables.get(type),),
            "Country" : 'SELECT * FROM %s WHERE ID="' % (dbTables.get(type),),
            "UserNote" : 'SELECT ID,attribution,details,status,visible,AsText(feature_geometry) FROM %s WHERE ID="' % (dbTables.get(type),),
            "error" : ''
        }

    db = {
        'table' : str(dbTables.get(type)),
        'query' : str(dbqs.get(type))
    }

    # Dictionary of edit history tables
    updateFuncs = {
            "PortChar" : updatePortChar,
            "PortInfraPoly" : updatePortPoly,
            "BasinPoly" : updatePortPoly,
            "AvoidPoly" : updatePortPoly,
            "BermAvoidPoly" : updatePortPoly,
            "StartEndPoly" : updatePortPoly,
            "PortPoly" : updatePortPoly,
            "Country" : updatePortChar,
            "UserNote" : updatePortChar,
            "error" : ''
        }

    # Print content-type header
    print GeoUtils.Interface.ContentType("html")
    print

    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
    try:
        print str(handleData(db=db,updateFunc=updateFuncs.get(type),fields=formFields.get(type),type=type,qv=qv,ge_key=ge_key))
    except:
        import sys,traceback
        print '<h3>Unexpected error:</h3>\n<br/><br/>\n<pre>\n'
        print traceback.format_exc()
        print '\n</pre>\n'

    print GeoUtils.Interface.StdHTMLFooter()

    # Close database
    DBhandle.close()

