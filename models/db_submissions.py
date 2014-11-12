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
                Field('file_name'),
                Field('homework', 'reference homework'),
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

def has_submitted(user_id, homework_id):
    student = (db.submission.id_student == user_id)
    submission = (db.submission.homework == homework_id)
    student_submission_count = db(student & submission).count()
    if student_submission_count > 0:
        return True
    return False

def can_submit(homework):
    if (request.now > homework.opening_date):
        return True
    return False

def empty_feedback(feedback_id):
    count = db(feedback_id == db.feedback.id).count()
    if count == 0:
        return True
    else:
        return False

def get_grade(homework_id):
    assignment = (db.assignment_grade.assignment_id == homework_id)
    user = (auth.user_id == db.assignment_grade.user_id)
    record = db(assignment & user).select().first()
    if record is not None:
        return int(record.grade)
    else:
        return None

def get_points(homework_id, section_id):
    homework = (db.homework.id == homework_id)
    section = (section_id == db.homework.course_section)
    record = db(homework & section).select().first()
    if record is not None:
        return record.points
    else:
        return None
