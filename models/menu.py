# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('LMS',SPAN(299)),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.web2py.com/")
response.title = 'LMS299'

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    ('MyHome', False, URL('default', 'index')),
    ('Search', False, URL('default', 'search')),
    ('MyCourses',False,URL('default', 'courses'),[
            ('CSC299',False,URL()),
            ('CSC438',False,URL()),
            ('CSC402',False,URL()),
            ]),
    ('ThisCourse',False,URL('default','course'),[
            ('Discussion',False,URL()),
            ('Content',False,URL()),
            ('Dropbox',False,URL()),
            ('Classlist',False,URL()),
            ('Attendance',False,URL()),
            ('Chat',False,URL()),
            ('grade',False,URL('grade', 'index', args=1)),
            ]),
    
]

if "auth" in locals(): auth.wikimenu() 
