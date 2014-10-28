'''

To Do:
Add reference to course-specific layout. 
Add permissions for modifying/setting layouts.

'''

STUDENT, TEACHER = 'student', 'teacher'

NE = IS_NOT_EMPTY()

db.define_table('theme',
                Field('name', requires=NE),
                Field('URL', requires=NE))


if db(db.theme).isempty():
    db.theme.insert(name="Light Theme", 
                        URL = URL('static', 'css/bootstrap-light.min.css'))
    db.theme.insert(name="Dark Theme",
                        URL = URL('static', 'css/bootstrap-dark.min.css'))
    db.theme.insert(name="Default",
                        URL = URL('static', 'css/bootstrap-dark.min.css'))

if not session.current_theme:
    rows = db(db.theme.name=="Default").select()
    session.current_theme = rows[0].URL

