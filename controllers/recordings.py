# coding: utf8
#This is the controller for the class recordings module of LMS299

def index():
    section_id = request.args(0,cast=int)
    videos = db(db.recording.course_id==section_id).select()
    youtube_id='dQw4w9WgXcQ'
    return dict(youtube_id=youtube_id, videos=videos)

def view():
    video_id = request.args(0,cast=int)
    video = db(db.recording.id==video_id).select().first()
    return dict(video=video)

@auth.requires_login()
def create():

    return  dict()