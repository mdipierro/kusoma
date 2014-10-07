# -*- coding: utf-8 -*-

def index():
    """
    general welcome page
    """
    return dict()

def search():
    """
    allows visitors to search by course name, code and tags
    """
    form = SQLFORM.factory(Field('keyword',requires=NE)).process()
    if form.accepted:
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
    rows = my_sections(course_id, auth.user_id)
    return dict(course=course, rows=rows, current_sections=current_sections,
                past_sections=past_sections)

def section():
    """
    this one shows details about a course section
    """
    section_id = request.args(0,cast=int)
    section = db.course_section(section_id)
    course = section.course
    membership = db.membership(role='student',
                               auth_user=auth.user_id,
                               course_section=section_id)
    return dict(course=course, section=section, 
                membership=membership)

@auth.requires_login()
def signup():
    section_id = request.args(0,cast=int)
    db.membership.insert(role="student",
                         course_section=section_id,
                         auth_user=auth.user.id)
    redirect(URL('section',args=section_id))

@auth.requires_login()
def drop():
    section_id = request.args(0,cast=int)
    db((db.membership.role=="student")&
       (db.membership.course_section==section_id)&
       (db.membership.auth_user==auth.user.id)).delete()
    redirect(URL('section',args=section_id))

def members():
    """
    shows students and teachers and graders in a course section
    """
    section_id = request.args(0,cast=int)
    if not is_user_teacher(section_id, auth.user_id):
        session.flash = 'Not authorized'
        redirect(URL('section',args=section_id)) 
    section = db.course_section(section_id)
    course = section.course
    rows = get_section_users(section.id)
    return dict(course=course, section=section, rows=rows)    

@auth.requires_login()
def manage_courses():
    grid = SQLFORM.smartgrid(db.course)
    return dict(grid=grid)

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)

def wiki():
    """
    wiki page
    """
    return dict()
