@auth.requires_login()
def index():
    '''
        Display course for user
    '''
    user_id = auth.user_id

    courses = my_sections()

    return dict(courses=courses)

@auth.requires_login()
def manage_uploads():
    """
    Author: Curtis Weir
    Date: 10/22/14
    Display assignments for a course section to the user
    """
    section_id = request.args(0,otherwise=URL('index'))
    section = db.course_section[section_id]
    if not is_user_student(section_id) and not is_user_teacher(section_id):
        return dict(section_id=section_id, section=section, rejected="Permission denied. You are not in this course section.")
    add_section_menu(section_id)
    folders = db(db.folder.course_section == section_id).select()
    homeworks = db(db.homework.course_section == section_id).select(orderby=db.homework.assignment_order)
    return dict(folders=folders, homeworks=homeworks,
                section_id=section_id, user_id=auth.user_id,
                section=section, rejected=None)

@auth.requires_login()
def view_submissions():
    """
    Author: Curtis Weir
    Date: 10/22/14
    Display submissions for a course section to the teacher
    """
    section_id = request.args(0,cast=int,otherwise=URL('index'))
    section = db.course_section[section_id]
    if not is_user_teacher(section_id):
        return dict(section_id=section_id, section=section, rejected="Permission denied. You are not a member of this course section.")
    homework_id = request.args(1,cast=int,otherwise=URL('index'))
    submissions = (db.submission.homework == homework_id)
    students = (db.submission.id_student == db.auth_user.id)
    student_submissions = db(submissions & students).select()
    return dict(section_id=section_id, homework_id=homework_id, section=section,
                rejected=None, student_submissions=student_submissions)

@auth.requires_login()
def my_submission():
    """
    Author: Curtis Weir
    Date: 11/6/14
    Display a submission for a homework to the user
    """
    section_id = request.args(0,cast=int,otherwise=URL('index'))
    section = db.course_section[section_id]
    if not is_user_student(section_id):
        return dict(section_id=section_id, section=section, rejected="Permission denied. You are not a student of this course section.")
    homework_id = request.args(1,cast=int,otherwise=URL('index'))
    if not has_submitted(auth.user_id, homework_id):
        return dict(section_id=section_id, section=section, rejected="Permission denied. You have not yet made a submission for this homework.")
    submission = (db.submission.homework == homework_id)
    student = (db.submission.id_student == auth.user_id)
    student_submission = db(submission & student).select().first()
    feedback = db(student_submission.id == db.feedback.id_submission).select().first()
    return dict(section_id=section_id, section=section, rejected=None,
                student_submission=student_submission, feedback=feedback)



def download():
    return response.download(request, db)

def uploading():
    record = db.attachment(request.args(0))
    db.attachment.insert(file_upload = 'text.txt')
    form = SQLFORM(db.attachment, record, deletable=True,
                  upload=URL('download'))
    if form.process().accepted:
       response.flash = 'form accepted'
       redirect(URL('index'))
    return form

@auth.requires_login()
def feedback():
    '''
        Sets feedback for assignment
    '''
    submission_id = request.args(0)
    section_id = request.args(1)
    homework_id = request.args(2)

    feedback = db(db.feedback.id_submission == submission_id).select().first()

    homework = db(db.homework.id == homework_id).select().first()

    db.feedback.date_added.writable = False
    db.feedback.date_added.readable = False
    db.feedback.id_submission.readable = False
    db.feedback.id_submission.writable = False
    db.feedback.id.readable = False
    form = SQLFORM(db.feedback, feedback)
    form.vars.id_submission = submission_id
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('view_submissions', args=[section_id, homework_id]))

    return dict(form=form, homework=homework)

@auth.requires_login()
def submit():
    section_id = request.args(0)
    homework_id = request.args(1)
    if (section_id is None or homework_id is None):
        redirect(URL('index'))
    student = (db.submission.id_student == auth.user_id)
    submission = (db.submission.homework == homework_id)
    record = db(student & submission).select().first()
    db.submission.id.readable = False
    db.submission.id_student.readable = False
    db.submission.id_student.writable = False
    db.submission.file_name.readable = False
    db.submission.file_name.writable = False
    db.submission.homework.readable = False
    db.submission.homework.writable = False
    form = SQLFORM(db.submission, record, upload=URL('download'))
    form.vars.id_student = auth.user_id
    if request.vars.file_upload is not None:
        try:
            form.vars.file_name = request.vars.file_upload.filename
        except:
            pass
    form.vars.homework = homework_id
    btn = form.element("input",_type="submit")
    if (record is not None):
        btn["_onclick"] = "return confirm('Are you sure you want to overwrite your submission?');"
    if form.process().accepted:
        redirect(URL('manage_uploads', args=(section_id)))
        response.flash = 'File submitted'
    elif form.errors:
        response.flash = 'Error file not submitted'
    return dict(form=form)
