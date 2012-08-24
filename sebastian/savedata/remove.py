#!/usr/bin/python
# David Newell
# sebastian/savedata/remove.py
# Handle and deleted selected data

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
def handleData(db,fields,qv,type,ge_key=""):
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
    
    # Get item ID
    if 'ID' in qv:
        id = qv['ID'].value
    else:
        id = 0
    
    # Deleted entry
    deleted = False
    
    # If type contains poly, run deletePortPoly function
    if 'Poly' in type:
        deleted = deletePortPoly(db,id,user,type)
    else:
        # Start delete database query
        delq = 'DELETE FROM %s WHERE ID="%s"' % (db['table'],id)
        
        # Delete entry from database
        deldata,delrc = DBhandle.query(delq)
        
        deleted = True
    
    if deleted:
        # Build ok message
        msg = '<h3>Success:</h3>\n<p>Deletion complete! Thanks for your entry.</p>\n'
        
        # Output ok message
        output = GeoUtils.Interface.uniForm.fullOkMsgGen(msg)
        
        # Return output
        return output
    else:
        # Build error message
        msg = '<h3>Error:</h3>\n<p>There was an error while deleting the item. Please try again.</p>\n'
        
        # Output error message
        output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)
        
        # Return output
        return output


# Update Port Polygon
def deletePortPoly(db,id,user,type):
    # Select old entry query
    selq = 'SELECT portID,timestamp,attribution,feature_type,feature_area,feature_perimeter,AsText(feature_geometry) FROM %s WHERE ID="%s"' % (db['table'],id)
    
    # Select old entry
    seld,selrc = DBhandle.query(selq)
    
    # If not only one entry, return incomplete deletion
    if selrc == 0 or selrc > 1:
        return False
    
    # First (only) row of database response
    d = seld[0]
    
    # Start delete database query
    delq = 'DELETE FROM %s WHERE ID="%s"' % (db['table'],id)
    
    # Start historical feature query
    histq = 'INSERT INTO historical_features (portID,created,attribution,feature_type,feature_geometry,feature_area,feature_perimeter) '
    histq += 'VALUES ("%(portID)s","%(timestamp)s","%(attribution)s","%(feature_type)s",GeomFromText("%(AsText(feature_geometry))s"),"%(feature_area)s","%(feature_perimeter)s")' % d
    
    # Delete old entry
    deld,delrc = DBhandle.query(delq)
    
    # Insert historical feature into history
    hd,hrc = DBhandle.query(histq)
    
    # Return success
    return True




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
            "StartEndPoly" : 'current_features',
            "PortPoly" : 'current_features',
            "error" : ''
        }
    
    formFields = {
            "PortChar" : GeoUtils.data.FormDicts.DeleteForm,
            "PortInfraPoly" : GeoUtils.data.FormDicts.DeleteForm,
            "BasinPoly" : GeoUtils.data.FormDicts.DeleteForm,
            "AvoidPoly" : GeoUtils.data.FormDicts.DeleteForm,
            "StartEndPoly" : GeoUtils.data.FormDicts.DeleteForm,
            "PortPoly" : GeoUtils.data.FormDicts.DeleteForm,
            "error" : ''
        }
    
    db = {
        'database' : 'uws_ge',
        'table' : str(dbTables.get(type))
    }
    
    # Print content-type header
    print GeoUtils.Interface.ContentType("html")
    print
    
    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
    
    if qv["AreYouSure"].value == 'Yes':
        try:
            print str(handleData(db=db,fields=formFields.get(type),type=type,qv=qv,ge_key=ge_key))
        except:
            import sys,traceback
            print '<h3>Unexpected error:</h3>\n<br/><br/>\n<pre>\n'
            print traceback.format_exc()
            print '\n</pre>\n'
    else:
        msg = '<h3>Error:</h3>\n'
        msg += '<p>If you really wish to delete this item, please try again and say so!</p>\n'
        print GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)
    
    print GeoUtils.Interface.StdHTMLFooter()
    
    # Close database
    DBhandle.close()

