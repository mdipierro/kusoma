

def index():

    #session.flash = "Select a theme for your LMS"
    
    rows = db(db.theme.name).select()

    return dict(rows = rows)


def theme_picked():

    '''
    Build the url to the css style page from arg, 
    and assign it to session.current_theme
    '''
    static_subfolder = request.args(0)
    css_filename = request.args(1)
    
    css_pathname = static_subfolder + '/'  + css_filename
    session.current_theme = URL('static', css_pathname)

    redirect(URL('themes', 'index'))    

    return dict()

def preview():
    
    subfolder = request.args(0)
    filename = request.args(1)

    session.preview_theme = subfolder + '/' + filename
    return dict()
