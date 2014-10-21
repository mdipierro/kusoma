#Author: Curtis Weir
#Date:   10/16/14

from gluon.tools import Auth
auth = Auth(db)

#My chrombook is being dumb, so I can't upload the whole repo :/
#Delete this if you have the db1.py in the app
db.define_table('course',
                Field('name', 'string'))

"""
Organize assignments
"""
db.define_table('folder',
                Field('name', 'string', requires=IS_NOT_EMPTY()))

"""
Assignment that pertains to a course
**Should we make this by course section instead?**
"""
db.define_table('assignments',
                Field('title', 'string', requires=IS_NOT_EMPTY()),
                Field('id_folder', 'reference folder'),
                Field('id_course', 'reference course'),
                Field('score', 'double'),
                Field('opening_date', 'datetime', default=request.now),
                Field('due_date', 'datetime'))

"""
File attached to an assignment
"""
db.define_table('attachment',
                Field('file_upload', 'upload', requires=IS_NOT_EMPTY()),
                Field('id_assignments', 'reference assignments'))

"""
Contains file submissions for students
"""
db.define_table('submission',
                Field('file_upload', 'upload', requires=IS_NOT_EMPTY()),
                Field('id_assignments', 'reference assignments'),
                Field('grade', 'double'),
                Field('id_student', 'reference auth_user', default=auth.user_id))

"""
Feedback given for a submission
"""
db.define_table('feedback',
                Field('comments', 'text', requires=IS_NOT_EMPTY()),
                Field('date_added', 'datetime', default=request.now),
                Field('id_submission', 'reference submission', requires=IS_NOT_EMPTY()))

db.assignments.id_folder.requires = IS_EMPTY_OR(IS_IN_DB(db, db.folder.id, '%(name)s'))
db.assignments.id_course.requires = IS_IN_DB(db, db.course.id, '%(name)s')

db.attachment.id_assignments.requires = IS_IN_DB(db, db.assignments.id, '%(title)s')

db.submission.id_assignments.requires = IS_IN_DB(db, db.assignments.id, '%(title)s')

db.feedback.id_submission.requires = IS_IN_DB(db, db.submission.id)
