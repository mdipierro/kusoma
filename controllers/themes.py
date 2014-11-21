

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

    session.prev_theme = session.current_theme
    
    css_pathname = static_subfolder + '/'  + css_filename
    session.css_pathname = css_pathname
    session.current_theme = URL('static', css_pathname)

	# Get the rows for this css, can just reuse URL as identifier
    picked = db(db.theme.URL == css_pathname).select()
    
    # Get the first use_count for the first row (there should only be one...)
    uses = int(picked[0].use_count) + 1

	# This update syntax works
    db(db.theme.URL == css_pathname).update(use_count=uses)

    #redirect(URL('themes', 'index'))    
    redirect(URL('themes', 'countdown'))

    return dict()

def countdown():
    return dict()

'''
If user rejects theme, they get sent here
'''
def themeBack():

    # delete 1 from theme count for the reject theme
    rejected_theme = db(db.theme.URL == session.css_pathname).select()
    uses = int(rejected_theme[0].use_count) - 1
    db(db.theme.URL == session.css_pathname).update(use_count=uses)

    #reset theme back to previous
    session.current_theme = session.prev_theme
    session.prev_theme = ''
    redirect(URL('themes', 'index'))
    return dict()

def display_popular():
    for row in db(db.theme).select(db.theme.name, orderby=db.theme.use_count*-1, limitby=(0, 3)):
        row.name, row.use_count


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

