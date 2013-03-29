#!/usr/bin/python
# David Newell
# sebastian/savedata/add.py
# Handle and save new data

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
def handleData(newFunc,db,fields,qv,type,ge_key=""):
    # Dictionary of functions to generate form field
    fieldRetr = {
            'text'     : GeoUtils.Interface.uniForm.textRetr,
            'textarea' : GeoUtils.Interface.uniForm.textareaRetr,
            'radio'    : GeoUtils.Interface.uniForm.radioRetr,
            'select'   : GeoUtils.Interface.uniForm.selectRetr,
            'hidden'   : GeoUtils.Interface.uniForm.hiddenRetr
        }

    # Get user name associated with given key
    DBhandle.setConnUserKey(ge_key)
    user = DBhandle.ConnUserName()

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

    new = newFunc(db,user,type,form)

    return new


# Update Port Characteristics
def newPortChar(db,user,type,f):
    # Start field names and values strings
    fieldNames = ''
    fieldValues = ''

    for k,v in f.iteritems():
        # Skip field names not in database
        if k in ["PortChar","Submit","GE_KEY"]:
            continue
        fieldNames += '%s,' % (k,)
        fieldValues += '"%s",' % (v,)

    # Start new entry database query, stripping final commas from fieldNames and fieldValues
    newq = 'INSERT INTO %s (%s) VALUES (%s)' % (db['table'],fieldNames[:-1],fieldValues[:-1])

    # Update database
    nd,nrc = DBhandle.query(newq)

    # Build ok message
    msg = '<h3>Success:</h3>\n<p>Your update succeeded! Thanks for your entry.</p>\n'

    # Output ok message
    output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)

    # Return output
    return output


# Update Port Polygon
def newPortPoly(db,user,type,f):
    # Skip new entry because of no geometry update
    if not 'feature_geometry' in f:
        # Start error message
        msg = '<h3>Error:</h3>\n<p>Invalid KML was submitted for this polygon. Please try again.</p>\n'

        # Output error message
        output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)

        # Return output
        return output

    # Define polygon holder variable
    poly = None

    # Convert KML to MySQL geometries
    for k in f:
        if k == 'feature_geometry':
            try:
                poly = GeoUtils.Features.Polygon()
                poly.fromKML(f['feature_geometry'])
                f[k] = poly.toMySQL_polygon()
            except:
                # Start error message
                msg = '<p>There was an error processing your request: invalid KML was submitted for this item. Please try again.</p>\n'

                # Return error
                return msg

    # Polygon area
    if poly == None:
        polyArea = "-9999"
        polyPerimeter = "-9999"
    else:
        polyArea = poly.area()
        polyPerimeter = poly.perimeter()

    # Start new entry database query
    newq = 'INSERT INTO %s (portID,attribution,feature_type,feature_geometry,feature_area,feature_perimeter) ' % (db['table'],)
    newq += 'VALUES ("%s","%s","%s",GeomFromText("%s"),"%s","%s")' % (f['portID'],user,f['feature_type'],f['feature_geometry'],polyArea,polyPerimeter)

    # Update database with new entry
    nd,nrc = DBhandle.query(newq)

    # Build ok message
    msg = '<h3>Success:</h3>\n<p>Your update succeeded! Thanks for your entry.</p>\n'

    # Output ok message
    output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)

    # Return output
    return output


# Create User Note
def newUserNote(db,user,type,f):
    # Skip new entry because of no geometry update
    if not 'feature_geometry' in f:
        # Start error message
        msg = '<h3>Error:</h3>\n<p>Invalid KML was submitted for this polygon. Please try again.</p>\n'

        # Output error message
        output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)

        # Return output
        return output

    # Convert KML to MySQL geometries
    for k in f:
        if k == 'feature_geometry':
            try:
                poly = GeoUtils.Features.Point()
                poly.fromKML(f[k])
                f[k] = poly.toMySQL_point()
            except:
                # Start error message
                msg = '<p>There was an error processing your request: invalid KML was submitted for this item. Please try again.</p>\n'

                # Output error message
                output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)

                # Return output
                return output

    # Start new entry database query
    newq = 'INSERT INTO %s (attribution,details,status,visible,feature_geometry) ' % (db['table'],)
    newq += 'VALUES ("%s","%s","%s",%s,GeomFromText("%s"))' % (user,f['details'],f['status'],f['visible'],f['feature_geometry'])

    # Update database with new entry
    nd,nrc = DBhandle.query(newq)

    # Build ok message
    msg = '<h3>Success:</h3>\n<p>Your note has been added! Thanks for your entry.</p>\n'

    # Output ok message
    output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)

    # Return output
    return output


# Create Data Request
def newRequest(db,user,type,f):
    # Start field names and values strings
    fieldNames = ''
    fieldValues = ''

    for k,v in f.iteritems():
        fieldNames += str(k) + ','
        fieldValues += '"' + str(v) + '",'

    # Start new entry database query, stripping final commas from fieldNames and fieldValues
    newq = 'INSERT INTO %s (%s) VALUES (%s)' % (db['table'],fieldNames[:-1],fieldValues[:-1])

    # Update database
    nd,nrc = DBhandle.query(updateq)

    # Build ok message
    msg = '<h3>Success:</h3>\n<p>Your update succeeded! Thanks for your entry.</p>\n'

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
            "UserNote" : 'notes',
            "DataRequest" : 'data_request',
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
            "UserNote" : GeoUtils.data.FormDicts.UserNote,
            "DataRequest" : GeoUtils.data.FormDicts.DataRequest,
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
            "UserNote" : 'ID',
            "DataRequest" : '',
            "error" : ''
        }

    dbqs = {
            "PortChar" : 'SELECT * FROM %s WHERE ID="' % (dbTables.get(type),),
            "PortInfraPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details FROM %s WHERE ID="' % (dbTables.get(type),),
            "BasinPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details FROM %s WHERE ID="' % (dbTables.get(type),),
            "AvoidPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details FROM %s WHERE ID="' % (dbTables.get(type),),
            "BermAvoidPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details FROM %s WHERE ID="' % (dbTables.get(type),),
            "StartEndPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details FROM %s WHERE ID="' % (dbTables.get(type),),
            "PortPoly" : 'SELECT ID,portID,timestamp,attribution,feature_type,AsText(feature_geometry),feature_details FROM %s WHERE ID="' % (dbTables.get(type),),
            "DataRequest" : 'SELECT latitude,longitude FROM %s WHERE ID="' % (dbTables.get("PortChar"),),
            "error" : ''
        }

    db = {
        'table' : str(dbTables.get(type)),
        'query' : str(dbqs.get(type))
    }

    # Dictionary of edit history tables
    newFuncs = {
            "PortChar" : newPortChar,
            "PortInfraPoly" : newPortPoly,
            "BasinPoly" : newPortPoly,
            "AvoidPoly" : newPortPoly,
            "BermAvoidPoly" : newPortPoly,
            "StartEndPoly" : newPortPoly,
            "PortPoly" : newPortPoly,
            "UserNote" : newUserNote,
            "DataRequest" : newRequest,
            "error" : ''
        }

    # Print content-type header
    print GeoUtils.Interface.ContentType("html")
    print

    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
    try:
        print str(handleData(db=db,newFunc=newFuncs.get(type),fields=formFields.get(type),type=type,qv=qv,ge_key=ge_key))
    except:
        import sys,traceback
        print '<h3>Unexpected error:</h3>\n<br/><br/>\n<pre>\n'
        print traceback.format_exc()
        print '\n</pre>\n'
    print GeoUtils.Interface.StdHTMLFooter()

    # Close database
    DBhandle.close()

