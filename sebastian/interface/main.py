#!/usr/bin/python
# David Newell
# interface/main.py
# Main interface to display in Google Earth via iframe

# Import Useful Modules
import sys, os
sys.path.append(os.path.abspath('../'))
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL
debug = 0

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
    output = ''

    # Query database for port details
    portq = "SELECT ID,name,latitude,longitude,sim_ready,defense_volume,defense_cement,defense_gravel,defense_sand,defense_engineer,analysis_complete,grid_height,grid_width,measured_defense_length,calculated_defense_length,measured_avg_defense_elevation,calculated_avg_defense_elevation FROM portdata WHERE ID='%s'" % (id,)
    portdata,portrowcount = DBhandle.query(portq)

    if portrowcount == 0 or portrowcount > 1:
        port_sim_ready = 0
        port_defense_volume = 0
        port_defense_cement = 0
        port_defense_gravel = 0
        port_defense_sand = 0
        port_defense_engineer = 0
        port_analysis_complete = 0
        port_grid_height = 0
        port_grid_width = 0
        port_measured_defense_length = 0
        port_calculated_defense_length = 0
        port_measured_avg_defense_elevation = 0
        port_calculated_avg_defense_elevation = 0
        port_dike_volume = 0
        port_core_volume = 0
        port_toe_volume = 0
        port_foundation_volume = 0
        port_armor_volume = 0
        port_timestamp = '0'
    else:
        port_sim_ready = float(portdata[0]['sim_ready'])
        port_defense_volume = float(portdata[0]['defense_volume'])
        port_defense_cement = float(portdata[0]['defense_cement'])
        port_defense_gravel = float(portdata[0]['defense_gravel'])
        port_defense_sand = float(portdata[0]['defense_sand'])
        port_defense_engineer = float(portdata[0]['defense_engineer'])
        port_analysis_complete = float(portdata[0]['analysis_complete'])
        port_grid_height = float(portdata[0]['grid_height'])
        port_grid_width = float(portdata[0]['grid_width'])
        port_measured_defense_length = float(portdata[0]['measured_defense_length'])
        port_calculated_defense_length = float(portdata[0]['calculated_defense_length'])
        port_measured_avg_defense_elevation = float(portdata[0]['measured_avg_defense_elevation'])
        port_calculated_avg_defense_elevation = float(portdata[0]['calculated_avg_defense_elevation'])
        port_dike_volume = 0
        port_core_volume = 0
        port_toe_volume = 0
        port_foundation_volume = 0
        port_armor_volume = 0
        port_timestamp = 0

    # Query database for port details
    simq = "SELECT ID as sim_id, path_volume, path_length, grid_height, grid_width, dike_volume, core_volume, toe_volume, foundation_volume, armor_volume, timestamp FROM portprotector WHERE portID='%s'" % (id,)
    simdata,simrowcount = DBhandle.query(simq)



    if simrowcount == 0 or simrowcount > 1:
        sim_id = 0
        sim_sim_ready = 0
        sim_defense_volume = 0
        sim_defense_cement = 0
        sim_defense_gravel = 0
        sim_defense_sand = 0
        sim_defense_engineer = 0
        sim_analysis_complete = 0
        sim_grid_height = 0
        sim_grid_width = 0
        sim_measured_defense_length = 0
        sim_calculated_defense_length = 0
        sim_measured_avg_defense_elevation = 0
        sim_calculated_avg_defense_elevation = 0
        sim_dike_volume = 0
        sim_core_volume = 0
        sim_toe_volume = 0
        sim_foundation_volume = 0
        sim_armor_volume = 0
        sim_timestamp = 0
    else:
        sim_id = float(simdata[0]['sim_id'])
        sim_sim_ready = 1
        sim_defense_volume = float(simdata[0]['path_volume'])
        sim_defense_cement = 0
        sim_defense_gravel = 0
        sim_defense_sand = 0
        sim_defense_engineer = 0
        sim_analysis_complete = 0
        sim_measured_defense_length = 0
        sim_calculated_defense_length = float(simdata[0]['path_length'])
        sim_measured_avg_defense_elevation = 0
        sim_calculated_avg_defense_elevation = 0
        sim_grid_height = float(simdata[0]['grid_height'])
        sim_grid_width = float(simdata[0]['grid_width'])
        sim_dike_volume = float(simdata[0]['dike_volume'])
        sim_core_volume = float(simdata[0]['core_volume'])
        sim_toe_volume = float(simdata[0]['toe_volume'])
        sim_foundation_volume = float(simdata[0]['foundation_volume'])
        sim_armor_volume = float(simdata[0]['armor_volume'])
        sim_timestamp = (simdata[0]['timestamp'])

    if (debug) :
        output += '<br/><table border=1>'
        output += '<tr>'
        output += '<td>&nbsp;</td><td>%i</td><td>%i</td>' % (id, sim_id, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%f</td><td>%f</td>' % ('grid_height', port_grid_height, sim_grid_height, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%f</td><td>%f</td>' % ('grid_width', port_grid_width, sim_grid_width, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('sim_ready', port_sim_ready, sim_sim_ready, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td><b>%.3e</b></td>' % ('c_def_le/pa_le', port_calculated_defense_length, sim_calculated_defense_length, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td><b>%.3e</b></td><td>%.1f</td>' % ('m_def_le', port_measured_defense_length, sim_measured_defense_length, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td><b>%.3e</b></td><td><b>%.3e</b></td>' % ('def_vol/path_vol', port_defense_volume, sim_defense_volume, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('defense_cement', port_defense_cement, sim_defense_cement, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('defense_gravel', port_defense_gravel, sim_defense_gravel, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('defense_sand', port_defense_sand, sim_defense_sand, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('defense_eng', port_defense_engineer, sim_defense_engineer, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('analysis_comp', port_analysis_complete, sim_analysis_complete, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('m_avg_def_el', port_measured_avg_defense_elevation, sim_measured_avg_defense_elevation, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('c_avg_def_el', port_calculated_avg_defense_elevation, sim_calculated_avg_defense_elevation, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td><b>%.3e</b></td>' % ('dike_volume', port_dike_volume, sim_dike_volume, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('core_volume', port_core_volume, sim_core_volume, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('toe_volume', port_toe_volume, sim_toe_volume, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('founda_vol', port_foundation_volume, sim_foundation_volume, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%.1f</td><td>%.1f</td>' % ('armor_volume', port_armor_volume, sim_armor_volume, )
        output += '</tr>'
        output += '<tr>'
        output += '<td>%s</td><td>%s</td><td><b>%s</b></td>' % ('timestamp', port_timestamp, sim_timestamp, )
        output += '</tr>'

        output += '</table>'

    output += '<h2>Welcome to Sebastian, SUPERSLR\'s GeoData Management System</h2>\n'

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

