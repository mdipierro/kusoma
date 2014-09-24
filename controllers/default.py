# -*- coding: utf-8 -*-

def index():
    return dict()

def search():
    form = SQLFORM.factory(Field('keyword',requires=NE)).process()
    if form.accepted:
        query = db.course.name.contains(form.vars.keyword)
        query = query|db.course.tags.contains(form.vars.keyword)
        rows = db(query).select(orderby=db.course.name)
    else:
        rows = ''
    return dict(form=form, rows=rows)

def course():
    course_id = request.args(0,cast=int)
    course = db.course(course_id) or redirect(URL('search'))
    return dict(course=course)

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)

