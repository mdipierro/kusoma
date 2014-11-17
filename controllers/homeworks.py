"""
Author: Curtis Weir
Date: 11/12/14
Display and manage homework assignments
"""
@auth.requires_login()
def manage_homeworks():
    section_id = request.args(0,otherwise=URL('index'))
    if not is_user_student(section_id) and not is_user_teacher(section_id):
        return dict(section_id=section_id, rejected="Permission denied. You are not in this course section.")
    db.homework.course_section.readable = False
    db.homework.course_section.writable = False
    db.homework.id.readable = False
    db.homework.id.writable = False
    db.homework.opening_date.represent = lambda value, row: value.strftime("%b %d, %Y %I:%S%p") if value is not None else "---"
    db.homework.due_date.represent = lambda value, row: value.strftime("%b %d, %Y %I:%S%p") if value is not None else "---"
    if is_user_student(section_id):
        db.homework.assignment_order.readable = False
        db.homework.course_section.default = section_id
        homeworks = SQLFORM.grid(db.homework.course_section == section_id,
                                 deletable=False, editable=False, create=False,
                                 args=request.args[:1],
                                 links = [lambda row: A('Submit Assignment',
                                                        _href=URL("dropbox","submit",args=[row.course_section, row.id]))] )
        rejected = None
    else:
        db.homework.course_section.default = section_id
        homeworks = SQLFORM.grid(db.homework.course_section == section_id, args=request.args[:1])
        rejected = None
    return locals()

@auth.requires_login()
def manage_folders():
    section_id = request.args(0,otherwise=URL('index'))
    if not is_user_teacher(section_id):
        return dict(section_id=section_id, rejected="Permission denied. You are the teacher of this course section.")
    db.folder.course_section.readable = False
    db.folder.course_section.writable = False
    db.folder.course_section.default = section_id
    folders = SQLFORM.grid(db.folder.course_section == section_id, args=request.args[:1])
    rejected = None
    return locals()