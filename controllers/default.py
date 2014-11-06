# -*- coding: utf-8 -*-

def index():
    """
    general welcome page
    """
    courses = db(db.course).select(limitby=(0,10),orderby='<random>')
    return dict(courses = courses)

def search():
    """
    allows visitors to search by course name, code and tags
    """
    form = FORM('Serch',INPUT(_name='keyword',requires=NE),_method='GET')
    if form.accepts(request.get_vars):
        query = db.course.name.contains(form.vars.keyword)
        query = query|db.course.code.contains(form.vars.keyword)
        query = query|db.course.tags.contains(form.vars.keyword)
        rows = db(query).select(orderby=db.course.name)
    else:
        rows = ''
    return dict(form=form, rows=rows)

def course():
    """
    allows to look at course description
    """
    import datetime
    today = datetime.date.today()
    course_id = request.args(0,cast=int)
    course = db.course(course_id) or redirect(URL('search'))
    sections = db(db.course_section.course==course.id).select()
    current_sections = [s for s in sections if s.stop_date>=today]
    past_sections = [s for s in sections if s.stop_date<today]
    rows = my_sections(course_id = course_id)
    return dict(course=course, rows=rows, current_sections=current_sections,
                past_sections=past_sections)

def section():
    """
    this one shows details about a course section
    """
    section_id = request.args(0,cast=int) # http://.../lms/default/section/3
    section = db.course_section(section_id) or redirect(URL('search'))
    add_section_menu(section_id)
    course = section.course
    membership = db.membership(role='student',
                               auth_user=auth.user_id,
                               course_section=section_id)
    return dict(course=course, section=section, 
                membership=membership)

@auth.requires_login()
def enroll():
    section_id = request.args(0,cast=int)
    n = db((db.membership.role=="student")&
           (db.membership.course_section==section_id)&
           (db.membership.auth_user==auth.user.id)).delete()
    if n==0:
        db.membership.insert(role="student",
                             course_section=section_id,
                             auth_user=auth.user.id)
        return 'Drop this class'        
    else:
        return 'Sign Up for this class'


@auth.requires_login()
def students():
    """
    shows students and teachers and graders in a course section
    """
    section_id = request.args(0,cast=int)
    if not (is_user_teacher(section_id) or auth.user.is_administrator):
        session.flash = 'Not authorized'
        redirect(URL('section',args=section_id)) 
    add_section_menu(section_id)
    section = db.course_section(section_id)
    course = section.course
    students = users_in_section(section_id,roles=[STUDENT])
    return dict(course=course, section=section, students=students)    

@auth.requires(auth.user and auth.user.is_administrator)
def manage_users():
    return dict(grid=SQLFORM.smartgrid(db.auth_user))

@auth.requires(auth.user and auth.user.is_administrator)
def manage_courses():
    return dict(grid=SQLFORM.smartgrid(db.course))

def section_docs():
    """
    shows students and teachers and graders in a course section
    """
    section_id = request.args(0,cast=int)
    section = db.course_section(section_id)
    db.doc.course_section.default = section_id
    form = SQLFORM(db.doc).process()
    docs = db(db.doc.course_section==section_id).select()
    return locals()

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)

def calendar():
    """
    allows to look at course description
    """
    import datetime
    today = datetime.date.today()
    course_id = request.args(0,cast=int)
    course = db.course(course_id) or redirect(URL('search'))
    sections = db(db.course_section.course==course.id).select()
    current_sections = [s for s in sections if s.stop_date>=today]
    past_sections = [s for s in sections if s.stop_date<today]
    rows = my_sections(course_id, auth.user_id)
    return dict(course=course, rows=rows, current_sections=current_sections,
                past_sections=past_sections)

