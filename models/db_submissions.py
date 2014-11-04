#Author: Curtis Weir
#Date:   10/16/14

from gluon.tools import Auth
auth = Auth(db)

"""
Assignment that pertains to a course
"""
db.define_table('assignments',
                Field('title', 'string', requires=IS_NOT_EMPTY()),
                Field('id_folder', 'reference folder'),
                Field('id_course', 'reference course_section'),
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
                Field('homework', 'reference homework'),
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

db.submission.homework.requires = IS_IN_DB(db, db.homework.id, '%(name)s')

db.feedback.id_submission.requires = IS_IN_DB(db, db.submission.id)

def folder_is_empty(folder, homeworks):
    for homework in homeworks:
        if homework.folder == folder.id:
            return False
    return True
