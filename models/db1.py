# TODO
#  Fix mapping tables to use joins.
#  
# ROLES = ('teacher','student','auditor','grader')

ROLE_TEACHER = 'teacher'
ROLE_STUDENT = 'student'
ROLE_AUDITOR = 'auditor'
ROLE_GRADER = 'grader'
ROLE_ADMINISTRATOR = 'administrator'

NE = IS_NOT_EMPTY()

# Populate the default roles.
if db(db.auth_group).isempty():
    db.auth_group.bulk_insert([{'role':ROLE_TEACHER},
                               {'role':ROLE_STUDENT},
                               {'role':ROLE_ADMINISTRATOR},
                               {'role':ROLE_AUDITOR},
                               {'role':ROLE_GRADER}])

db.define_table(
    'course',
    Field('name',requires=NE),
    Field('code',requires=NE),
    Field('prerequisites','list:string'),  # This should be a reference to another course.
    Field('description','text'),
    Field('tags','list:string'),
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
    format='%(name)s')

db.define_table(
    'membership',
    Field('course_section','reference course_section'),
    Field('auth_user','reference auth_user'),
    Field('role','reference auth_group'),
    auth.signature)

db.define_table(
    'doc',
    Field('name',requires=NE),
    Field('course_section','reference course_section',writable=False,readable=False),
    Field('filename','upload',label='Content'),   
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
             (db.membership.auth_user==user_id)&
             (db.membership.role==db.auth_group.id))
    return db(query).select()

def get_section_users(section_id):
    query = (db.membership.course_section==section_id)&(db.membership.auth_user==db.auth_user.id)
    return db(query).select()

def is_user_teacher(section_id, user_id):
    return db((db.membership.course_section==section_id) &
              (db.membership.role==teacher_group_id()) &
              (db.membership.auth_user==user_id)).count() > 0

def is_user_administrator(user_id):
    admin_group_id = db(db.auth_group.role == ROLE_ADMINISTRATOR).select().first().id
    return db((db.auth_membership.user_id == user_id) &
              (db.auth_membership.group_id == admin_group_id)).count() > 0

def is_student_in_section(section_id, user_id):
    count = db((db.membership.course_section == section_id) &
              (db.membership.role == student_group_id()) &
              (db.membership.auth_user == user_id)).count()
    return count > 0

def students_in_section(section_id):
    return db((db.membership.course_section == section_id) &
              (db.membership.role == student_group_id()) &
              (db.membership.auth_user == db.auth_user.id)).select(db.auth_user.id,
                                                                   db.auth_user.first_name,
                                                                   db.auth_user.last_name)

def students_in_course(course_id):
    return db((db.course.id == course_id) &
              (db.course.id == db.course_section.course) &
              (db.membership.course_section == db.course_section.id) &
              (db.membership.role == student_group_id()) &
              (db.membership.auth_user == db.auth_user.id)).select(db.auth_user.id,
                                                                   db.auth_user.first_name,
                                                                   db.auth_user.last_name)

def student_group_id():
    return db(db.auth_group.role == ROLE_STUDENT).select().first().id

def teacher_group_id():
    return db(db.auth_group.role == ROLE_TEACHER).select().first().id

def administrator_group_id():
    return db(db.auth_group.role == ROLE_ADMINISTRATOR).select().first().id

####################################################################################################
# Populate some tables so we have data with which to work.
if db(db.auth_user).isempty():
    import datetime
    from gluon.contrib.populate import populate
    mdp_id = db.auth_user.insert(first_name="Massimo",last_name='Di Pierro',
                                 email='massimo.dipierro@gmail.com',
                                 password=CRYPT()('test')[0])

    db.auth_membership.insert(user_id=mdp_id, group_id=teacher_group_id())
    db.auth_membership.insert(user_id=mdp_id, group_id=student_group_id())
                              
    populate(db.auth_user,500)

    # Add everyone in the auth_user table - except Massimo - to the student group.
    for person_id in db(db.auth_user.id != mdp_id).select():
        db.auth_membership.insert(user_id=person_id, group_id=student_group_id())

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
                                 role=teacher_group_id())
            for row in rows:
                db.membership.insert(course_section=i,
                                     auth_user=row.id,
                                     role=student_group_id())

# add logic to add me and massimo to the admin and teacter groups
# students = db((db.auth_user.first_name != 'Massimo') | (db.auth_user.first_name != 'Bryan')).select(db.auth_user.id)
# for student in students:
#     db.auth_membership.insert(user_id=student.id, group_id=2)
####################################################################################################
