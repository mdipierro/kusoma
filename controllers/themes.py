

def index():

    session.flash = "Select a theme for your LMS"
    
    return dict(themes = SQLFORM.grid(db.theme.name))

