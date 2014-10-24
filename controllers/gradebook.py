# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def manage_grades():
    section_id=request.args(0, cast=int)

    if not (is_user_teacher(section_id) or auth.user.is_aministrator):
        session.flash = 'Not authorized'
        redirect(URL('student',args=section_id))

    redirect(URL('teacher',args=section_id))
    return dict()

@auth.requires_login()
def teacher():
    session_id = request.args(0, cast=int)
    if not (is_user_teacher(session_id)):
        session.flash = 'Not authorized'
        redirect(URL('student',args=section_id))

    response.files.insert(0,URL('static','js/jquery.js'))
    response.files.insert(0,URL('static','js/jquery.handsontable.full.js'))
    response.files.insert(0,URL('static','css/jquery.handsontable.full.css'))
    response.files.insert(0,URL('static','css/grading.css'))

    session.flash = 'Welcome Teacher'


    student = get_all_students(session_id)
    return dict(role="Teacher", users= student)

@auth.requires_login()
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

@auth.requires_login()
def savedata():
    import gluon.contrib.simplejson
    data = gluon.contrib.simplejson.loads(request.body.read())
    return response.json(data)
