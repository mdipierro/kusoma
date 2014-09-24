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

#from gluon.contrib.populate import populate
#populate(db.auth_user,100)

#auth.enable_record_versioning(db)
    
    
