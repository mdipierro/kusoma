def index():
    return dict()

@auth.requires_login()
def course_dropbox():
    """
    Author: Curtis Weir
    Date: 10/22/14
    Display assignments for a course section to the user
    """
    section_id = request.args(0,cast=int)
    if not is_user_student(section_id) and not is_user_teacher(section_id):
        return dict(section_id=section_id, rejected="Permission denied. You are not in this course section.")
    section = db.course_section[section_id]
    add_section_menu(section_id)
    folders = db(db.folder.course_section == section_id).select()
    homeworks = db(db.homework.course_section == section_id).select()
    form = add_folder(section_id)
    return dict(folders=folders, homeworks=homeworks,
                section_id=section_id, user_id=auth.user_id,
                section=section, rejected=None, form=form)

def add_folder(section_id):
    """
    Creates a form to add a new folder.
    Returns a SQLFORM
    """
    form = SQLFORM(db.folder, fields=['name'])
    if form.process().accepted:
        db.folder.insert(name=form.vars.name, course_section=section_id)
        redirect(URL('course_dropbox',args=(section_id)))
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return form

@auth.requires_login()
def view_submissions():
    """
    Author: Curtis Weir
    Date: 10/22/14
    Display submissions for a course section to the teacher
    """
    section_id = request.args(0,cast=int)
    if not is_user_teacher(section_id):
        return dict(section_id=section_id, rejected="Permission denied. You are not the teacher of this course section.")
    section = db.course_section[section_id]
    homework_id = request.args(1,cast=int)
    homework = db.homework[homework_id]
    submissions = (db.submission.homework == db.homework.id)
    students = (db.submission.id_student == db.auth_user.id)
    student_submissions = db(submissions & students).select()
    return dict(section_id=section_id, section=section, rejected=None, student_submissions=student_submissions)

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
