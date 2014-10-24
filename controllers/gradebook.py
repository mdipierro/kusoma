# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def manage_grades():
    section_id = request.args(0, cast=int)
    session.flash = 'Welcome Student'
    section = db.course_section(section_id)
    section_name=section.name	
    member = db.membership(course_section=section_id, auth_user=auth.user.id)
    role = 'student' #role = db.auth_group(member.role)
    student_grades = db( (db.grade.section_id==section.id) & (db.grade.auth_user==auth.user.id)).select()
    return dict(section=section, member=member, role=role, student_grades=student_grades,section_id=section_id)

 
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
    section_id = request.args(0, cast=int)
    section = db.course_section(section_id)
    section_name=section.name	
    member = db.membership(course_section=section_id, auth_user=auth.user.id)
    role = 'student' #role = db.auth_group(member.role)
    student_grades = db( (db.grade.section_id==section.id) & (db.grade.auth_user==auth.user.id)).select()
    return dict(section=section, member=member, role=role, student_grades=student_grades)
    #return dict(role="student")


def savedata():
    import gluon.contrib.simplejson
    data = gluon.contrib.simplejson.loads(request.body.read())
    return response.json(data)
