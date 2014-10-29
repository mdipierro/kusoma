

def index():

    session.flash = "Select a theme for your LMS"
    
    themes = SQLFORM.grid(db.theme.name))
    themes.selectable = True

    return dict(themes = themes)

