#!/usr/bin/python
# David Newell
# GeoUtils/Interface/__init__.py
# Geographical Utilities Interface package initiation

import uniForm
import genKML


# ContentType
# Prints content type based on extension
def ContentType(extension):
    ExtensionContentTypes = {
            'kml' : 'Content-type: application/vnd.google-earth.kml+xml',
            'html' : 'Content-type: text/html',
            'txt' : 'Content-type: text/plain'
        }
    
    return ExtensionContentTypes.get(str(extension))

# StdHTMLHeader
# Prints out the usual HTML header
#   headerInfo - additional HTML to place in <head> tag
def StdHTMLHeader(headerInfo=""):
    html_header = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n'
    html_header += ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'
    html_header += '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n'
    html_header += '<head>\n'
    html_header += str(headerInfo) + '\n'
    html_header += '</head>\n<body>\n'

    return html_header

    
# StdHTMLFooter
# Prints out the usual HTML footer
def StdHTMLFooter():
    html_footer = "</body>\n</html>\n"
    
    return html_footer


# StdHTML
# Prints out the standard HTML
def StdHTML(headerInfo,content):
    html = StdHTMLHeader(headerInfo)
    html += '\n'
    html += str(content)
    html += '\n'
    html += StdHTMLFooter()
    
    return html



# StdKMLHeader
# Prints out the usual KML header
def StdKMLHeader():
    kml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_header += '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
    kml_header += '<Document>\n'

    return kml_header

    
# StdKMLFooter
# Prints out the usual KML footer
def StdKMLFooter():
    kml_footer = '</Document>\n'
    kml_footer += '</kml>\n'
    
    return kml_footer


# StdKML
# Prints out the standard KML
def StdKML(content):
    kml = StdKMLHeader()
    kml += '\n'
    kml += str(content)
    kml += '\n'
    kml += StdKMLFooter()
    
    return kml


# Build buttons
# buttons - dictionary with button information
# options - values for variable options
def buildButtons(buttons,options):
    # Start output
    output = ''
    
    # Add buttons to action list
    for i in buttons:
        # Begin link
        output += '<a href="'
        output += str(buttons[i][1]) + '?'
        
        # Add each variable option to query string
        for o in buttons[i][2]:
            # If blank, continue to next value
            if o == '':
                continue
            
            # Add option to query string
            output += str(o) + '=' + str(options.get(o)) + '&'
        
        # Add each specified option to query string
        for o in buttons[i][3]:
            # If blank, continue to next value
            if o == '':
                continue
            
            # Add option to query string
            output += str(o) + '=' + str(buttons[i][3].get(o)) + '&'
        
        # Strip last ampersand, if last character is an ampersand
        if output[len(output)-1] == '&':
            output = output[:-1]
        
        # Add label and close link
        output += '" class="button"><span class="' + str(buttons[i][0]) + '">' + i + '</span></a>\n'
    
    return output

# buildButton
# Writes and individual button.
# text - The button text
# type - What kind of button (For styling)
# target - href target script
# variables - a dictionary of variable options used as inputs to the target script
def buildButton(text, type, target, variables):
    output = '<a href="'
    output += str(target) + '?'
    
    for v in variables:
        # if blank continue
        if v == '':
            continue

        output += str(v) + '=' + str(variables.get(v)) + '&'
    
    # Strip last ampersand 
    if output[len(output) - 1] == '&':
        output = output[:-1]
    
    # Add label and close link
    output += '" class="button"><span class="' + type + '">' + text + '</span></a>\n'

    return output



