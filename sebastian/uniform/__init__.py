#!/usr/bin/python
# David Newell
# uniform/__init__.py
# Field generation formatted for use with uni-form


def textGen(options,id,label,value,hint):
    # Text field formatted with uni-form 
    field = '<div class="ctrlHolder">\n'
    field += '<label for="' + str(id) + '">' + str(label) + '</label>\n'
    field += '<input name="' + str(id) + '" id="' + str(id) + '" value="' + str(value) + '" size="35" maxlength="25" type="text" class="textInput" '
    
    if 'readonly' in options:
        field += 'readonly="readonly" '
    if 'disabled' in options:
        field += 'disabled="disabled" '
    
    field +=' />\n'
    
    if not hint == '':
        field += '<p class="formHint">' + str(hint) + '</p>\n'
    
    field += '</div>\n'
    
    # Return formatted field
    return field



def textareaGen(options,id,label,value,hint):
    # Text field formatted with uni-form 
    field = '<div class="ctrlHolder">\n'
    field += '<label for="' + str(id) + '">' + str(label) + '</label>\n'
    field += '<textarea name="' + str(id) + '" id="' + str(id) + '"  '
    
    if 'rows' in options:
        field += 'rows="' + str(options['rows']) + '" '
    if 'cols' in options:
        field += 'cols="' + str(options['cols']) + '" '
    
    field +=' >\n'
    field += str(value)
    field += '</textarea>\n'
    
    if not hint == '':
        field += '<p class="formHint">' + str(hint) + '</p>\n'
    
    field += '</div>\n'
    
    # Return formatted field
    return field



def selectGen(options,id,label,value,hint):
    # Drop-down selection formatted with uni-form 
    field = '<div class="ctrlHolder">\n'
    field += '<label for="' + str(id) + '">' + str(label) + '</label>\n'
    field += '<select name="' + str(id) + '" id="' + str(id) + '">\n'
    
    for i in options:
        field += '<option value="' + str(i) + '"'
        if i == value:
            field += ' selected="selected"'
        field += '>' + str(options[i]) + '</option>\n'
    
    field += '</select>\n'
    
    if not hint == '':
        field += '<p class="formHint">' + str(hint) + '</p>\n'
    
    field += '</div>\n'
    
    # Return formatted field
    return field



def radioGen(options,id,label,value,hint):
    # Radio buttons formatted with uni-form
    field = '<div class="ctrlHolder">\n'
    field += '<p class="label">' + str(label) + '</p>\n' 
    field += '<div class="multiField">\n'
    
    for i in options:
        field += '<label for="' + str(id) + str(i) + '" class="blockLabel"><input name="' + str(id) + '" id="' + str(id) + str(i) + '" value="' + str(i) + '" '
        
        if value == options[i]:
            field += 'checked="checked" '
        
        field += 'type="radio" />' + str(i) + '</label>\n'
    
    if not hint == '':
        field += '<p class="formHint">' + str(hint) + '</p>\n'
    
    field += '</div>\n' 
    field += '</div>\n'
    
    # Return formatted radio buttons
    return field



def buttonGen(id,type,label):
    # Button formatted with uni-form
    button = '<button type="' + str(type) + '" class="' + str(type) + 'Button" id="' + str(id) + '" name="' + str(id) + '">'
    button += str(label)
    button += '</button>\n'
    
    # Return button
    return button



def hiddenGen(id,value):
    # Hidden field (no formatting necessary)
    field = '<input type="hidden" name="'
    field += str(id)
    field += '" id="'
    field += str(id)
    field += '" value="'
    field += str(value)
    field += '" />\n'
    
    # Return formatted hidden field
    return field



def errorGen(text):
    # Error message formatted with uni-form
    message = '<div id="errorMsg">\n' 
    message += text
    message += '</div>\n'
    
    # Return formatted error message
    return message



def fullErrorMsgGen(text):
    # Error message formatted with uni-form
    message = '<form action="#" class="uniForm">\n'
    message += errorGen(text)
    message += '</form>\n'
    
    # Return formatted error message
    return message



def okGen(text):
    # OK message formatted with uni-form
    message = '<div id="OKMsg">\n' 
    message += text
    message += '</div>\n'
    
    # Return formatted error message
    return message



def fullOkMsgGen(text):
    # Error message formatted with uni-form
    message = '<form action="#" class="uniForm">\n'
    message += okGen(text)
    message += '</form>\n'
    
    # Return formatted error message
    return message



def textRetr(entry,options):
    # Retrieve entered value in text box
    value = entry.value
    
    # Return value
    return value



def textareaRetr(entry,options):
    # Retrieve entered value in text area
    value = entry.value
    
    # Return value
    return value



def selectRetr(entry,options):
    # Retrieve entered value in select (drop-down) box
    v = entry.value
    
    if v in options:
        value = options[v]
    
    # Return value
    return value



def radioRetr(entry,options):
    # Retrieve entered value in radio buttons
    v = entry.value
    
    if v in options:
        value = options[v]
    
    # Return value
    return value



def hiddenRetr(entry,options):
    # Retrieve entered value in hidden field
    value = entry.value
    
    # Return value
    return value


