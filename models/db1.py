# TODO
#  Fix mapping tables to use joins.
#  
# ROLES = ('teacher','student','auditor','grader')

from os import path

STUDENT, TEACHER = 'student','teacher'

NE = IS_NOT_EMPTY()

db.define_table('theme',
                Field('name', requires=NE),
                Field('URL', requires=NE), 
                Field('image_URL', requires=NE),
                Field('use_count', default=0))

db.define_table('image',
    Field('name', requires=NE),
    Field('thumbfile', 'upload', uploadfolder=path.join(
        request.folder,'static','photo_gallery'
        ), autodelete=True, label=T('ThumbFile'))
)

if db(db.image).isempty():
    db.image.insert(name="Light Theme", 
                        thumbfile = 'light.jpg')
    db.image.insert(name="Dark Theme",
                        thumbfile = 'dark.jpg')
    db.image.insert(name='Bluish',
                        thumbfile = 'bluish.jpg')
    db.image.insert(name='Maverick',
                        thumbfile = 'maverick.jpg')
    db.image.insert(name='Sky Blue',
                        thumbfile = 'skyblue.jpg')
    db.image.insert(name='Sunny Hill',
                        thumbfile = 'sunnyhill.jpg')
    db.image.insert(name="Default",
                        thumbfile = 'default.jpg')


if db(db.theme).isempty():
    db.theme.insert(name="Light Theme", 
                    URL = 'css/bootstrap-light.min.css',
                    image_URL = 'images/light.jpg')
    db.theme.insert(name="Dark Theme",
                    URL = 'css/bootstrap-dark.min.css', 
                    image_URL = 'images/dark.jpg')
    db.theme.insert(name='Bluish',
                    URL = 'css/bootstrap-bluish.min.css', 
                    image_URL = 'images/bluish.jpg')
    db.theme.insert(name='Maverick',
                    URL = 'css/bootstrap-pinkish.min.css', 
                    image_URL = 'images/maverick.jpg')
    db.theme.insert(name='Sky Blue',
                    URL = 'css/bootsrap-pinkish.min.css', 
                    image_URL = 'images/skyblue.jpg')
    db.theme.insert(name='Sunny Hill',
                    URL = 'css/bootstrap-sunnyhill.min.css', 
                    image_URL = 'images/sunnyhill.jpg')
    db.theme.insert(name="Default",
                    URL = 'css/bootstrap-responsive.min.css', 
                    image_URL = 'images/default.jpg')


# To be used later. Adds foreign key to themes table
#ADVANCED = True
ADVANCED = False
course_fields = [
    Field('name',requires=NE),
    Field('code',requires=NE),
    # This should be a reference to another course.
    Field('prerequisites','list:string'),  
    Field('description','text'),
    Field('tags','list:string')]
if ADVANCED:    
    course_fields.append(Field('theme', 'reference theme', default=1))
    
db.define_table(
    'course',
    *course_fields,
    **dict(format='%(code)s: %(name)s'))

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
    Field('role', requires=IS_IN_SET((STUDENT, TEACHER))),
    auth.signature)

db.define_table(
    'doc',
    Field('name',requires=NE),
    Field('course_section','reference course_section',writable=False,readable=False),
    Field('filename','upload',label='Content'),   
    auth.signature)

"""
Organize homeworks into folders for a particular class section
"""
db.define_table(
    'folder',
    Field('name', 'string', requires=NE),
    Field('course_section', 'reference course_section'))

db.define_table(
    'homework',
    Field('name',requires=NE),
    Field('course_section','reference course_section'),
    Field('folder', 'reference folder',
          requires=IS_EMPTY_OR(IS_IN_DB(db,'folder.id','%(name)s'))),
    Field('description','text'),
    Field('opening_date', 'datetime', default=request.now),
    Field('due_date','datetime'),
    Field('filename','upload'),
    Field('points', 'integer'),
    Field('assignment_order', 'integer'),
    format='%(name)s')

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

def my_sections(user_id=auth.user_id, course_id=None, roles=[TEACHER, STUDENT],max_sections=20):
    """
    returns a Rows of Sections the user_id is in in any of the speficied roles (teacher or student)
    if a course_id is specified it returns only sections for that course id (default to all courses)
    if max_sections is specified limits the search results (defaults to 20)
    """
    query = ((db.membership.course_section==db.course_section.id)&
             (db.membership.auth_user==user_id)&
             (db.membership.role.belongs(roles)))
    if course_id:
        query &= db.course_section.course==course_id
    return db(query).select(db.course_section.ALL,limitby=(0,max_sections))

def is_user_student(section_id, user_id=auth.user_id):
    """
    checks if the user_id (or the current user) is enrolled in the section_id as a student
    """
    return db((db.membership.course_section==section_id) &
              (db.membership.role==STUDENT) &
              (db.membership.auth_user==user_id)).count() > 0

def is_user_teacher(section_id, user_id=auth.user_id):
    """
    checks if the user_id (or the current user) is the teacher of a the section_id
    """
    return db((db.membership.course_section==section_id) &
              (db.membership.role==TEACHER) &
              (db.membership.auth_user==user_id)).count() > 0

def users_in_section(section_id,roles=[STUDENT]):
    """
    returns a list of users with a role (default STUDENT role) in the section_id    
    """
    return db((db.membership.course_section == section_id) &
              (db.membership.role.belongs(roles))&
              (db.membership.auth_user == db.auth_user.id)).select(db.auth_user.ALL)

####################################################################################################
# Populate some tables so we have data with which to work.
if db(db.auth_user).isempty():
    import datetime
    from gluon.contrib.populate import populate
    mdp_id = db.auth_user.insert(first_name="Good",last_name='Teacher',
                                 email='good.teacher@example.com',
                                 password=CRYPT()('test')[0])
    st_id = db.auth_user.insert(first_name="Good",last_name='student',
                                 email='good.student@example.com',
                                 password=CRYPT()('test')[0])


    populate(db.auth_user,300)
    db(db.auth_user.id>1).update(is_student=True,is_teacher=False,is_administrator=False)


    # Add everyone in the auth_user table - except Massimo - to the student group.
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
            db.membership.insert(course_section=i, auth_user=mdp_id, role=TEACHER)
            db.membership.insert(course_section=i, auth_user=st_id, role=STUDENT)

            for h in range(1,7):
                db.homework.insert(name='hw'+str(h), course_section=i,points=10, assignment_order=h)

            for row in rows:
                db.membership.insert(course_section=i, auth_user=row.id, role=STUDENT)


# add logic to add me and massimo to the admin and teacter groups
# students = db((db.auth_user.first_name != 'Massimo') | (db.auth_user.first_name != 'Bryan')).select(db.auth_user.id)
# for student in students:
#     db.auth_membership.insert(user_id=student.id, group_id=2)
####################################################################################################
