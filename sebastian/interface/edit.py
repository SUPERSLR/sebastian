#!/usr/bin/python
# David Newell
# interface/edit.py
# Data edit (form) interface to display in Google Earth via iframe

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Connect to database
DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')


# Generate form
# db - dictionary of database information (Format: {'database' : 'value' , 'query' : 'value'}
# fields - dictionary with fieldset and field information
# type - item type
# id - item ID (default: 0)
# ge_key - user identification key
# edit - permission to edit, 1/0 -> yes/no (default: 0)
def formGen(db,fields,type,id=0,ge_key="",edit=0):
        # Query database
        print '<br/>000 db<br/>'
        print db
        print '<br/>0001 db[query]<br/>'
        print db['query']
        dbdata,rowcount = DBhandle.query(db['query'])

        # If more than one row or no rows returned, raise error
        if rowcount > 1 or rowcount == 0:
                # Return error
                error = "%s database rows returned from edit history." % (rowcount,)

                # Build error message
                msg = '<h3>There was an error while processing your request, please try again later.</h3>\n'
                msg += '<p>If you believe you have received this message in error, please ensure you have correctly downloaded your access file correctly.</p>\n'
                msg += '<p>For all other questions or comments, please contact us (%s), including the information below.</p>\n' % (GeoUtils.constants.contactEmail,)
                msg += '<p><em>%s</em></p>\n' % (error,)

                # Output error message
                output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)

                # Function exits
                return output

        # Record is first (only) row of data
        r = dbdata[0]

        # Convert NAN/-9999 values to blanks
        for k in r:
                if r[k] == -9999 or r[k] == "-9999":
                        r[k] = ""

        # Dictionary of functions to generate form field
        fieldGen = {
                        'text' : GeoUtils.Interface.uniForm.textGen,
                        'textarea' : GeoUtils.Interface.uniForm.textareaGen,
                        'radio' : GeoUtils.Interface.uniForm.radioGen,
                        'select' : GeoUtils.Interface.uniForm.selectGen,
                        'button' : GeoUtils.Interface.uniForm.buttonGen,
                        'hidden' : GeoUtils.Interface.uniForm.hiddenGen,
                        'errMsg' : GeoUtils.Interface.uniForm.errorGen
                }

        # Form header
        output = '<form action="%(BASE_URL)s/savedata/update.py" method="get" name="%(type)s-%(id)s" id="%(type)s-%(id)s" class="uniForm inlineLabels">\n' % {'BASE_URL' : BASE_URL , 'type' : type , 'id' : id}

        fsk = fields.keys()
        fsk.sort()

        for set in fsk:
                print '111<br/>'
                print set
                if set == 'zbuttons':
                        # If no permission to edit, display error message instead of submit button
                        if edit == 0:
                                # Build error message
                                msg = '<h3>You do not have permission to edit this feature.</h3>\n'
                                msg += '<p>If you believe you have received this message in error, please ensure you have correctly downloaded your access file correctly.</p>\n'
                                msg += '<p>For all other questions or comments, please contact us (%s).</p>\n' % (GeoUtils.constants.contactEmail,)

                                # Add formatted error message to output
                                output += fieldGen.get('errMsg')(msg)
                        else:
                                output += '<div class="buttonHolder">\n'
                                for button in fields[set]:
                                        print '222<br/>'
                                        print button
                                        output += fieldGen.get('button')(id=button,type=fields[set][button][0],label=fields[set][button][1])
                                output += '</div>\n'
                elif set == 'zhidden':
                        # For each hidden field, add to output
                        for f,o in fields[set].iteritems():
                                if o[3] == "GE_KEY":
                                        output += fieldGen.get('hidden')(f,str(ge_key))
                                elif o[3] == "itemType":
                                        output += fieldGen.get('hidden')(f,str(type))
                                else:
                                        output += fieldGen.get('hidden')(f,str(o[3]))
                else:
                        # Start fieldset
                        output += '<fieldset>\n'

                        # Legend (header)
                        output += '<legend>%s</legend>\n' % (set,)

                        # For each field in set,
                        for f,o in fields[set].iteritems():
                                print '<br/>333 f<br/>'
                                print f
                                print '<br/>444 o<br/>'
                                print o
                                print '<br/>4441 o[3]<br/>'
                                print o[3]
                                print '<br/>4442 r<br/>'
                                print r
                                print '<br/>4443 r[o[3]]<br/>'
                                print r[o[3]]
                                # If geometry specified, assume new geometry entry and set to blank
                                if str(o[3]) == 'feature_geometry' or str(o[3]) == '':
                                        value = ''
                                else:
                                        value = r[o[3]]

                                # Get edit history item time
                                eTs = {
                                           'PortChar' : 'PortChar',
                                           'PortInfraPoly' : 'PortPoly',
                                           'BasinPoly' : 'PortPoly',
                                           'AvoidPoly' : 'PortPoly',
                                           'BermAvoidPoly' : 'PortPoly',
                                           'StartEndPoly' : 'PortPoly',
                                           'PortPoly' : 'PortPoly',
                                           'Region' : 'Region',
                                           'ModelPath' : 'None'
                                        }

                                eType = eTs.get(str(type),'')

                                # If edit information is not to be displayed, show only hint
                                if eType == 'None':
                                        # Set hint
                                        hint = o[4]
                                else:
                                        # Retrieve edit information from database
                                        editq = 'SELECT attribution,timestamp FROM edit_history WHERE itemID="%s" AND field="%s" AND type="%s" ORDER BY timestamp DESC' % (id,o[3],eType)
                                        editdata,editrowcount = DBhandle.query(editq)

                                        # If no edits found, display never edited by N/A, otherwise take most recent result (first result)
                                        if editrowcount == 0:
                                                e = {
                                                        'attribution' : 'N/A',
                                                        'timestamp' : 'never'
                                                }
                                        else:
                                                e = editdata[0]
                                                print '<br/>555 e<br/>'
                                                print e

                                        # Set hint
                                        hint = o[4] + '\n<br/>\n'

                                        # Add edited information to hint
                                        hint += '<em>Last edited %(timestamp)s by %(attribution)s</em>\n' % e

                                # Add formatted field to output
                                output += fieldGen.get(o[0])(options=o[2],id=f,label=o[1],value=value,hint=hint)
                                print '<br/>666 value<br/>'
                                print value

                        # Close fieldset
                        output += '</fieldset>\n'

        # Form footer
        output += '</form>\n'

        # Return form output
        return output



# If file called directly, output html
if __name__ == "__main__":
        # Print content-type header
        print GeoUtils.Interface.ContentType("html")
        print

        # Retrieve user information
        qv = []

        # Import cgi module to get query string
        import cgi

        qv = cgi.FieldStorage()

        try:
                type = str(qv["type"].value)
                id = int(qv["id"].value)
                ge_key = str(qv["GE_KEY"].value)
                edit = int(qv["edit"].value)
                error = 'None'
        except KeyError:
                type = 'error'
                id = 0
                ge_key = ''
                edit = 0
                error = KeyError

        formQuery = {
                        "PortChar" : 'SELECT * FROM portdata WHERE ID="%s"' % (id,),
                        "PortInfraPoly" : 'SELECT * FROM current_features WHERE ID="%s" AND feature_type="Port Infrastructure Polygon"' % (id,),
                        "BasinPoly" : 'SELECT * FROM current_features WHERE ID="%s" AND feature_type="Basin Polygon"' % (id,),
                        "AvoidPoly" : 'SELECT * FROM current_features WHERE ID="%s" AND feature_type="Model Avoid Polygon"' % (id,),
                        "BermAvoidPoly" : 'SELECT * FROM current_features WHERE ID="%s" AND feature_type="Berm Avoid Polygon"' % (id,),
                        "StartEndPoly" : 'SELECT * FROM current_features WHERE ID="%s" AND feature_type="Model StartEnd Polygon"' % (id,),
                        "Country" : 'SELECT * FROM countries WHERE ID="%s"' % (id,),
                        "ModelPath" : 'SELECT * FROM portprotector WHERE ID="%s"' % (id,),
                        "UserNote" : 'SELECT * FROM notes WHERE ID="%s"' % (id,),
                        "error" : 'SELECT * FROM portdata WHERE ID="0"'
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
                        "ModelPath" : GeoUtils.data.FormDicts.ModelPath,
                        "UserNote" : GeoUtils.data.FormDicts.UserNote,
                        "error" : ''
                }

        db = { 'query' : formQuery.get(type) }


        print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
        print "<br/>Debug Edit 01</br>"
        print id
        print formQuery
        print db
        print type
        print formFields
        print "<br/>Debug Edit 02</br>"
        print formFields.get(type)
        print "<br/>Debug Edit 03</br>"
        try:
                print formGen(db=db,fields=formFields.get(type),type=type,id=id,ge_key=ge_key,edit=edit)
        except:
                import sys,traceback
                print '<h3>Unexpected error:</h3>\n<br/><br/>\n<pre>\n'
                print traceback.format_exc()
                print '\n</pre>\n'

        print GeoUtils.Interface.StdHTMLFooter()

        # Close database
        DBhandle.close()

