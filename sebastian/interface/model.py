#!/usr/bin/python
# David Newell
# interface/model.py
# Model run (form) interface to display in Google Earth via iframe

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL


# Generate form
# fields - dictionary with fieldset and field information
# type - item type
# ge_key - user identification key
# edit - permission to edit, 1/0 -> yes/no (default: 0)
def formGen(fields,type,id,ge_key="",edit=0):
    # If no permission to edit, display error
    if edit == 0:
        # Start error message
        msg = '<h3>Error: You do not have permission to access this feature.</h3>\n'
        msg += '<p>If you believe you have received this message in error, please ensure you have correctly downloaded your access file correctly.</p>\n'
        msg += '<p>For all other questions or comments, please contact us (%s).</p>\n' % (GeoUtils.constants.contactEmail,)

        # Output error message
        output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)

        # Return formatted error information
        # Function exits
        return output

    # Function
    fieldGen = {
            'text' : GeoUtils.Interface.uniForm.textGen,
            'textarea' : GeoUtils.Interface.uniForm.textareaGen,
            'radio' : GeoUtils.Interface.uniForm.radioGen,
            'select' : GeoUtils.Interface.uniForm.selectGen,
            'button' : GeoUtils.Interface.uniForm.buttonGen,
            'hidden' : GeoUtils.Interface.uniForm.hiddenGen
        }

    # Form header
    output = '<form action="%s/model/portprotector.py" method="get" name="%s" id="%s" class="uniForm inlineLabels">\n' % (BASE_URL,type,type)

    fsk = fields.keys()
    fsk.sort()

    for set in fsk:
        if set == 'zbuttons':
            output += '<div class="buttonHolder">\n'
            for button in fields[set]:
                output += fieldGen.get('button')(id=button,type=fields[set][button][0],label=fields[set][button][1])
            output += '</div>\n'
        elif set == 'zhidden':
            # For each hidden field, add to output
            for f in fields[set]:
                if fields[set][f][3] == "GE_KEY":
                    output += fieldGen.get('hidden')(f,str(ge_key))
        else:
            # Start fieldset
            output += '<fieldset>\n'

            # Legend (header)
            output += '<legend>%s</legend>\n' % (set,)

            h = 0.25
            w = 0.25
            DBhandle = GeoUtils.RDB()
            DBhandle.connect('uws_ge')
            grid_query = "SELECT DISTINCT grid_height,grid_width FROM portdata WHERE id = %s" % (id,)
            portdata, count = DBhandle.query(grid_query)
            if portdata[0]['grid_height'] :
                h = portdata[0]['grid_height']
            if portdata[0]['grid_width'] :
                w = portdata[0]['grid_width']

            # For each field in set,
            for f in fields[set]:
                # Set value
                if 'GridHeight' in f:
                    value = h
                elif 'GridWidth' in f:
                    value = w
                elif 'ID' in f:
                    value = str(id)
                else:
                    value = ''

                # Set hint
                hint = fields[set][f][4]

                # Add formatted field to output
                output += fieldGen.get(fields[set][f][0])(options=fields[set][f][2],id=f,label=fields[set][f][1],value=value,hint=hint)

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
    try:
        import cgi
        qv = cgi.FieldStorage()

        type = str(qv["type"].value)
        ge_key = str(qv["GE_KEY"].value)
        id = int(qv["id"].value)
        edit = int(qv["edit"].value)
        error = 'None'
    except KeyError:
        type = 'error'
        ge_key = ''
        id = 0
        edit = 0
        error = KeyError

    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
    try:
        print formGen(fields=GeoUtils.data.FormDicts.PortProtectorModel,type=type,id=id,ge_key=ge_key,edit=edit)
    except:
        import sys,traceback
        print 'Unexpected error:<br/><br/>\n<pre>\n'
        print traceback.format_exc()
        print '\n</pre>\n'
    print GeoUtils.Interface.StdHTMLFooter()

