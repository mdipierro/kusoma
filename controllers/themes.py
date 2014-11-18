

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

	# Get the rows for this css, can just reuse URL as identifier
    picked = db(db.theme.URL == css_pathname).select()
    
    # Get the first use_count for the first row (there should only be one...)
    uses = int(picked[0].use_count) + 1

	# This update syntax works
    db(db.theme.URL == css_pathname).update(use_count=uses)

	
	
	# See table printed out, use_counts will increment. 
    all_rows = db(db.theme).select()
    print all_rows


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

