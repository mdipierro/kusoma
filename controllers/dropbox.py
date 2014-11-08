@auth.requires_login()
def index():
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
    section_id = request.args(0,cast=int)
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
    section_id = request.args(0,cast=int)
    section = db.course_section[section_id]
    if not is_user_teacher(section_id):
        return dict(section_id=section_id, section=section, rejected="Permission denied. You are not the teacher of this course section.")
    homework_id = request.args(1,cast=int)
    homework = db.homework[homework_id]
    submissions = (db.submission.homework == db.homework.id)
    students = (db.submission.id_student == db.auth_user.id)
    student_submissions = db(submissions & students).select()
    return dict(section_id=section_id, section=section, rejected=None, student_submissions=student_submissions)

@auth.requires_login()
def feedback():
    record = db.feedback(request.args(0))
    form = SQLFORM(db.feedback, record)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)


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

# coding: utf8
# try something like
def feedback():
    
 
   
    feedbacks = db.feedback(request.args(0))
    form = SQLFORM(db.feedback, feedbacks)
    db.feedback.date_added.writable = True
    return dict(form=form)
