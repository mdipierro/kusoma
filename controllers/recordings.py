# coding: utf8
#This is the controller for the class recordings module of LMS299

def index():
    section_id = request.args(0,cast=int)
    section=db(db.course_section.id == section_id).select().first()
    if not section: redirect(URL('default','index'))
    videos = db(db.recording.course_id==section_id).select()
    return dict(section=section, videos=videos)

def view():
    video_id = request.args(0,cast=int)
    video = db(db.recording.id==video_id).select().first()
    return dict(video=video)

@auth.requires_login()
def create():

    return  dict()
