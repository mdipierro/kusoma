'''

To Do:
Add reference to course-specific layout. 
Add permissions for modifying/setting layouts.

'''

STUDENT, TEACHER = 'student', 'teacher'

NE = IS_NOT_EMPTY()

db.define_table('theme',
                Field('name', requires=NE),
                Field('URL', requires=NE), 
                Field('image_URL', requires=NE))

#db(db.theme).delete()

if db(db.theme).isempty():
    db.theme.insert(name="Light Theme", 
                    URL = 'css/bootstrap-light.min.css',
                    image_URL = 'images/light.jpg')
    db.theme.insert(name="Dark Theme",
                    URL = 'css/bootstrap-dark.min.css', 
                    image_URL = 'images/dark.jpg')
    db.theme.insert(name='Bluish',
                    URL = 'css/bootstrap-bluish.min.css', 
                    image_URL = 'images/bluish.jpg')
    db.theme.insert(name='Maverick',
                    URL = 'css/bootstrap-pinkish.min.css', 
                    image_URL = 'images/maverick.jpg')
    db.theme.insert(name='Sky Blue',
                    URL = 'css/bootsrap-pinkish.min.css', 
                    image_URL = 'images/skyblue.jpg')
    db.theme.insert(name='Sunny Hill',
                    URL = 'css/bootstrap-sunnyhill.min.css', 
                    image_URL = 'images/sunnyhill.jpg')
    db.theme.insert(name="Default",
                    URL = 'css/bootstrap-responsive.min.css', 
                    image_URL = 'images/default.jpg')


if not session.current_theme:
    rows = db(db.theme.name=="Default").select()
    session.current_theme = URL('static', rows[0].URL)
