ROLES = ('teacher','student','auditor','grader')

NE = IS_NOT_EMPTY()

db.define_table(
    'course',
    Field('name',requires=NE),
    Field('code',requires=NE),
    Field('prerequisites','list:string'),
    Field('description','text'),
    Field('tags','list:string'),
    auth.signature,
    format='%(code)s: %(name)s')

db.define_table(
    'course_section',
    Field('name',requires=NE),
    Field('course','reference course'),
    Field('meeting_time','string'),
    Field('meeting_place','string'),
    Field('signup_deadline','date'),
    Field('drop_deadline','date'),
    Field('start_date','date'),
    Field('stop_date','date'),
    Field('syllabus','text'),
    Field('private_info','text'),
    Field('on_line','boolean',default=False,label='Online'),
    Field('inclass','boolean',default=True),
    auth.signature,
    format='%(name)s')

db.define_table(
    'membership',
    Field('course_section','reference course_section'),
    Field('auth_user','reference auth_user'),
    Field('role',requires=IS_IN_SET(ROLES)),
    auth.signature)

db.define_table(
    'occurrance',
    Field('name',requires=NE),
    Field('description','text'),
    Field('posted_datetime','datetime',default=request.now),
    Field('start_datetime','datetime',default=request.now),
    Field('stop_datetime','datetime',default=request.now),
    Field('course_section','reference course_section',
          requires=IS_EMPTY_OR(IS_IN_DB(db,'course_section.id','%(name)s'))),
    auth.signature)

def my_sections(course_id, user_id):
    query = ((db.course_section.course==course_id)&
             (db.membership.course_section==db.course_section.id)&
             (db.membership.auth_user==user_id))
    return db(query).select()

def get_section_users(section_id):
    query = (db.membership.course_section==section_id)&(db.membership.auth_user==db.auth_user.id)
    return db(query).select()

def is_user_teacher(section_id, user_id):
    return db.membership(course_section=section_id,
                         role='teacher',
                         auth_user=user_id)

## Given a section id and a user id, return true if user is a member of session
## false otherwise
def is_in_class(section_id, user_id):
    query = (db.membership.course_section==section_id)&(db.membership.auth_user==user_id)
    return len(db(query).select()) > 0

if db(db.auth_user).isempty():
    import datetime
    from gluon.contrib.populate import populate
    db.auth_user.insert(first_name="Massimo",last_name='Di Pierro',
                        email='massimo.dipierro@gmail.com',
                        password=CRYPT()('test')[0])
    populate(db.auth_user,500)
    for k in range(200,300):
        id = db.course.insert(name="Dummy course",
                              code="CSC%s" % k,
                              prerequisites=[],
                              tags=[],
                              description = 'description...')
        for s in range(701,703):
            i = db.course_section.insert(
                name="CSC%s-%s" % (k,s),
                course=id,
                meeting_place="CDM",
                meeting_time="Tuesday",
                start_date=datetime.date(2014,9,1),
                stop_date=datetime.date(2014,12,1),
                signup_deadline=datetime.date(2014,11,10))
            rows = db(db.auth_user).select(limitby=(0,10),orderby='<random>')
            db.membership.insert(course_section=i,
                                 auth_user=1,
                                 role='teacher')
            for row in rows:
                db.membership.insert(course_section=i,
                                     auth_user=row.id,
                                     role='student')

                         
    
    
