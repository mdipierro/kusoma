# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('LMS'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.web2py.com/")
response.title = 'Learning Management System'

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
    ('Search', False, URL('default', 'search'))]

if auth.user:
    courses = [(s.name,False,URL('default','section',args=s.id)) for s in my_sections()]
    if courses:
        response.menu.append(('My Courses',False,None,courses))

if auth.user and auth.user.is_administrator:
    response.menu.append(('Manage',False,None,[
                ('Users',False,URL('default','manage_users')),
                ('Courses',False,URL('default','manage_courses'))]))

def add_section_menu(section_id):
    response.menu.append(('Course Content',False,None,[
                ('Students',False,URL('default','students',args=section_id)),
                ('Homeworks',False,URL('homeworks','manage_homeworks',args=section_id)),
                ('Grades',False,URL('gradebook','manage_grades',args=section_id)),
                ('Quizzes',False,URL('quizzes','manage_quizzes',args=section_id)),
                ('Dropbox',False,URL('dropbox','index',args=section_id)),
                ('Chat',False,URL('chat','manage_chat',args=section_id)),
                ('Recordings',False,URL('recordings','index',args=section_id)),
                ]))

if False:    
    auth.wikimenu()
