# -*- coding: utf-8 -*-
# try something like
def index():
    return dict(message="hello just testing!!")

def teacher():
    response.files.insert(0,URL('static','js/jquery.js'))
    response.files.insert(0,URL('static','js/jquery.handsontable.full.js'))
    response.files.insert(0,URL('static','css/jquery.handsontable.full.css'))
    response.files.insert(0,URL('static','css/grading.css'))

    session.flash = 'Welcome Teacher'

    session_id = 1 #temp session Id s
    student = get_section_users(session_id)
    return dict(role="Teacher", users= student)

def student():
    session.flash = 'Welcome Student'
    return dict(role="student")


def savedata():
    import gluon.contrib.simplejson
    data = gluon.contrib.simplejson.loads(request.body.read())
    return response.json(data)


