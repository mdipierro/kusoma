

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

'''
user can set a course's theme here 

TODO: modify smartgrid to only show certain fields, 
join to themes table to show theme names
'''
@auth.requires(auth.user and auth.user.is_administrator)
def course_themes():
    grid=SQLFORM.smartgrid(db.course, linked_tables=['theme'])

    return dict(grid=grid)


