

def index():

    #session.flash = "Select a theme for your LMS"
    
    rows = db(db.theme.name).select()

    return dict(rows = rows)


def redirect():

    '''
    Build the url to the css style page from arg, 
    and assign it to session.current_theme
    '''
    static_subfolder = request.args(0)
    css_filename = request.args(1)
    
    css_pathname = static_subfolder + '/'  + css_filename
    session.current_theme = URL('static', css_pathname)

    ### redirect in 10 seconds, or give option to go back and choose different theme
    #redirect('http://www.google.com')

    return dict()
