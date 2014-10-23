def index():
    return dict()

def course_dropbox():
    """
    Author: Curtis Weir
    Date: 10/22/14
    Display assignments for a course section to the user
    """
    section_id = request.args(0,cast=int)
    if not is_user_student(section_id, auth.user_id) and not is_user_teacher(section_id, auth.user_id):
        return dict(rejected="Permission denied. You are not in this course section.")
    section = db.course_section[section_id]
    folders = db(db.folder.course_section == section_id).select()
    homeworks = db(db.homework.course_section == section_id).select()
    form=FORM('Add Folder: ', INPUT(_name='name', requires=IS_NOT_EMPTY()), INPUT(_type='submit'))
    if form.accepts(request,session):
        response.flash = 'Folder Added'
        db.folder.insert(name=form.vars.name, course_section=section_id)
        redirect(URL('course_dropbox',args=(section_id)))
    elif form.errors:
        response.flash = 'Form is empty.'
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

def uploading():
    record = db.attachment(request.args(0))
    db.attachment.insert(file_upload = 'text.txt')
    form = SQLFORM(db.attachment, record, deletable=True,
                  upload=URL('download'))
    if form.process().accepted:
       response.flash = 'form accepted'
       redirect(URL('index'))
    return form
