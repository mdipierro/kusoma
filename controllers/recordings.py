# coding: utf8
#This is the controller for the class recordings module of LMS299

@auth.requires_login()
def index():
    section_id = request.args(0,cast=int)
    section=db(db.course_section.id == section_id).select().first()
    if not section: redirect(URL('default','index'))
    videos = db(db.recording.course_id==section_id).select()
    if is_user_student(section_id):
        is_teacher=False
    elif is_user_teacher(section_id):
        is_teacher=True
    else:
        redirect(URL('default','section', args=section_id))
    return dict(section=section, videos=videos, is_teacher=is_teacher)

@auth.requires_login()
def view():
    video_id = request.args(0,cast=int)
    video = db(db.recording.id==video_id).select().first()
    section_id = video.course_id
    if not is_user_student(section_id) or not is_user_teacher(section_id):
        redirect(URL('default','section', args=section_id))
    return dict(video=video)

@auth.requires_login()
def create():
    return dict()
