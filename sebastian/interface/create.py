#!/usr/bin/python
# David Newell
# interface/create.py
# Data creation (form) interface to display in Google Earth via iframe

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
def formGen(fields,type,pid,ge_key="",edit=0):
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
    output = '<form action="%s/savedata/add.py" method="get" name="%s-%s" id="%s-%s" class="uniForm inlineLabels">\n' % (BASE_URL,type,id,type,id)
    
    fieldSets = fields.keys()
    fieldSets.sort()
    
    for set in fieldSets:
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
                if f == 'PortID':
                    value = str(pid)
                else:
                    # All fields are blank in create form
                    value = ''
                
                # Set hint
                hint = o[4]
                
                # Add formatted field to output
                output += fieldGen.get(o[0])(options=o[2],id=f,label=o[1],value=value,hint=hint)
            
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
        pid = int(qv["id"].value)
        ge_key = str(qv["GE_KEY"].value)
        edit = int(qv["edit"].value)
        error = 'None'
    except KeyError:
        type = 'error'
        pid = 0
        ge_key = ''
        edit = 0
        error = KeyError
    
    formFields = {
            "PortChar" : GeoUtils.data.FormDicts.PortChar,
            "PortInfraPoly" : GeoUtils.data.FormDicts.PortPoly,
            "BasinPoly" : GeoUtils.data.FormDicts.PortPoly,
            "AvoidPoly" : GeoUtils.data.FormDicts.PortPoly,
            "StartEndPoly" : GeoUtils.data.FormDicts.PortPoly,
            "PortPoly" : GeoUtils.data.FormDicts.PortPoly,
            "UserNote" : GeoUtils.data.FormDicts.UserNote,
            "error" : ''
        }
    
    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
    try:
        print formGen(fields=formFields.get(type),type=type,pid=pid,ge_key=ge_key,edit=edit)
    except:
        import sys,traceback
        print '<h3>Unexpected error:</h3>\n<br/><br/>\n<pre>\n'
        print traceback.format_exc()
        print '\n</pre>\n'
    
    print GeoUtils.Interface.StdHTMLFooter()
    


