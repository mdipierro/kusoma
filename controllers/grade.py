# -*- coding: utf-8 -*-
# try something like
def index():
    usr_id = auth.user.id;
    query = db.membership.auth_user == usr_id
    sections = db(query).select(orderby=db.membership.course_section)
  
    return dict(message="Your Course:", sections = sections)

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
    section_id = request.args(0,cast=int) 
    section = db.course_section(section_id)
    student_grades=db((db.grade.section_id==section.id) & (db.grade.auth_user==db.auth_user.id))
    return dict(role="student", student_grades=student_grades)


def savedata():
    import gluon.contrib.simplejson
    data = gluon.contrib.simplejson.loads(request.body.read())
    return response.json(data)
