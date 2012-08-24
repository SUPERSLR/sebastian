#!/usr/bin/python
# David Newell
# interface/main.py
# Main interface to display in Google Earth via iframe

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Connect to database
DBhandle = GeoUtils.RDB()
DBhandle.connect('uws_ge')


# Variable to enable debugging values
debugEnabled = False


# Generate interface for item
# id - id of type element (default: 0)
# ge_key - user identification key
# edit - permission to edit, 1/0 -> yes/no (default: 0) 
def ItemInterface(buttons,type,error,id=0,ge_key="",edit=0):
    # Options values dictionary
    options = {
            'id' : id,
            'type' : type,
            'GE_KEY' : ge_key,
            'edit' : edit
        }
    
    # Start output
    output = '<h2>Welcome to Sebastian, SUPERSLR\'s GeoData Management System</h2>\n'
    
    output += '<br/>\n'
    
    output += '<h3>Actions</h3>\n'
    
    # Get formatted buttons
    output += GeoUtils.Interface.buildButtons(buttons,options)
    
    # Return formatted output
    return output


# Generate interface for notes
# id - id of type element (default: 0)
# ge_key - user identification key
# edit - permission to edit, 1/0 -> yes/no (default: 0) 
def NoteInterface(buttons,type,error,id=0,ge_key="",edit=0):
    # Options values dictionary
    options = {
            'id' : id,
            'type' : type,
            'GE_KEY' : ge_key,
            'edit' : edit
        }
    
    # Start output
    output = '<h2>Welcome to Sebastian, SUPERSLR\'s GeoData Management System</h2>\n'
    
    output += '<br/>\n'
    
    output += '<h3>Note Details:</h3>\n<p>'
    
    # Build database query
    dbq = 'SELECT details FROM notes WHERE ID="%s"' % (id,)
    
    # Query database
    dbdata,rowcount = DBhandle.query(dbq)
    
    if rowcount == 0 or rowcount > 1:
        # Build error message
        msg += '<h3>Error:</h3>\n<p>There was an error retrieving the note details. Please try again.</p>\n'
        
        # Output error message
        output += GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)
    else:
        output += str(dbdata[0]['details'])
    
    
    output += '</p>\n<br/>\n'
    output += '<h3>Actions</h3>\n'
    
    # Get formatted buttons
    output += GeoUtils.Interface.buildButtons(buttons,options)
    
    # Return formatted output
    return output


# Generate interface for info balloons
# id - id of type element (default: 0)
# ge_key - user identification key
# edit - permission to edit, 1/0 -> yes/no (default: 0) 
def InfoInterface(buttons,type,error,id=0,ge_key="",edit=0):
    # Options values dictionary
    options = {
            'id' : id,
            'type' : type,
            'GE_KEY' : ge_key,
            'edit' : edit
        }
    
    # Start output
    output = '<h2>Welcome to Sebastian, SUPERSLR\'s GeoData Management System</h2>\n'
    
    output += '<br/>\n'
    
    output += '<p>Your username: <strong>'
    
    output += DBhandle.ConnUserName()
    output += '</strong></p>\n'
    
    output += '<p>For more information about Sebastian and the SUPERSLR project, please visit us at: '
    output += '<a href="http://www.seaports2100.org">http://www.seaports2100.org</a>'
    output += '</p>\n'
    
    output += '<br/>\n'
    output += '<h3>Actions</h3>\n'
    
    # Get formatted buttons
    output += GeoUtils.Interface.buildButtons(buttons,options)
    
    # Return formatted output
    return output


# Main Interface
# Displayed on error and in overview placemark
def MainInterface(buttons,type,error,id,ge_key="",edit=0):
    # If error has value, print error
    if not (error == "" or error == "None"):
        # Start error message
        msg = '<h3>There was an error while processing your request. Please try again later.</h3>\n'
        msg += '<p>If you continue to receive this error, please ensure you have correctly downloaded your access file correctly.</p>\n'
        msg += '<p>For all other questions, please contact us (%s), including the information below:</p>\n<br/>\n' % (GeoUtils.constants.contactEmail,)
        msg += '<p><em>Error Details</em></p>\n<br/><br/>\n'
        msg += '<ul>\n'
        msg += '<li>Type: %s</li>\n' % (type,)
        msg += '<li>ID: %s</li>\n' % (id,)
        msg += '<li>GE_KEY: %s</li>\n' % (ge_key,)
        msg += '<li>Edit: %s</li>\n' % (edit,)
        msg += '<li>Other: %s</li>\n' % (error,)
        msg += '</ul>\n'
        
        output = GeoUtils.Interface.uniForm.fullErrorMsgGen(msg)
        
        # Return formatted error message
        # Format output
        return output
    
    # Options values dictionary
    options = {
            'id' : id,
            'type' : type,
            'GE_KEY' : ge_key,
            'edit' : edit
        }
    
    # Start output
    output = '<h2>Welcome to Sebastian, SUPERSLR\'s GeoData Management System</h2>\n'
    
    output += '<br/>\n'
    output += '<h3>Actions</h3>\n'
    
    # Get formatted buttons
    output += GeoUtils.Interface.buildButtons(buttons,options)
    
    # Return formatted output
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
        item = str(qv["item"].value)
        type = str(item.split("-")[0])
        id = int(item.split("-")[1])
        ge_key = str(qv["GE_KEY"].value)
        error = 'None'
    except KeyError:
        type = 'error'
        id = 0
        ge_key = ''
        error = KeyError
        
        if debugEnabled:
            # Debugging values
            type = 'PortChar'
            id = 180
            ge_key = '14b9055d351595cc332c92eec2a06ebf'
            error = 'None'
    
    
    # Specify form types in dictionary to be called later
    # Structure: ("type", formFunc)
    interfaceTypes = {
            "PortChar" : ItemInterface,
            "PortInfraPoly" : ItemInterface,
            "BasinPoly" : ItemInterface,
            "AvoidPoly" : ItemInterface,
            "StartEndPoly" : ItemInterface,
            "ModelPath" : ItemInterface,
            "Country" : ItemInterface,
            "UserNote" : NoteInterface,
            "Info" : InfoInterface,
            "error" : MainInterface
        }
    
    # Specify form types in dictionary to be called later
    # Structure: ("type", formFunc)
    interfaceDicts = {
            "PortChar" : GeoUtils.data.InterfaceDicts.PortChar,
            "PortInfraPoly" : GeoUtils.data.InterfaceDicts.PortPoly,
            "BasinPoly" : GeoUtils.data.InterfaceDicts.PortPoly,
            "AvoidPoly" : GeoUtils.data.InterfaceDicts.PortPoly,
            "StartEndPoly" : GeoUtils.data.InterfaceDicts.PortPoly,
            "ModelPath" : GeoUtils.data.InterfaceDicts.ModelPath,
            "Country" : GeoUtils.data.InterfaceDicts.Country,
            "UserNote" : GeoUtils.data.InterfaceDicts.UserNote,
            "Info" : GeoUtils.data.InterfaceDicts.Main,
            "error" : GeoUtils.data.InterfaceDicts.Main
        }
    
    # Get user information and permissions
    DBhandle.setConnUserKey(ge_key)
    user = DBhandle.ConnUserName()
    edit = DBhandle.ConnUserPrivilege()
    
    
    print GeoUtils.Interface.StdHTMLHeader(GeoUtils.Interface.uniForm.HTMLHeaderInfo())
    try:
        print interfaceTypes.get(type,MainInterface)(buttons=interfaceDicts.get(type),type=type,error=error,id=id,ge_key=ge_key,edit=edit)
    except:
        import sys,traceback
        print 'Unexpected error:<br/><br/>\n<pre>\n'
        print traceback.format_exc()
        print '\n</pre>\n'
    print GeoUtils.Interface.StdHTMLFooter()
    
    # Close database
    DBhandle.close()

