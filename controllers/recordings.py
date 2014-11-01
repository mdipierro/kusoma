# coding: utf8
#This is the controller for the class recordings module of LMS299

@auth.requires_login()
def index():
    section_id = request.args(0,cast=int)
    section=db(db.course_section.id == section_id).select().first()
    if not section: redirect(URL('default','index'))
    
    add_section_menu(section_id)
    
    videos = db(db.recording.course_id==section_id).select()
    if is_user_student(section_id):
        is_teacher=False
    elif is_user_teacher(section_id):
        is_teacher=True
    else:
        redirect(URL('default','section', args=section_id))
    return dict(section=section, videos=videos, is_teacher=is_teacher)

@auth.requires_login()
def add_recording():
    '''
    This is a callback function to register a new recording.
    request.args[0]= The section_id
    request.args[1]= The youtube_id of the new recording
    
    Test example: Adds a recording to course_section 2
    Visit lms299/recordings/add_recording/2/aKdV5FvXLuI
    Then visit lms299/recordings/index/2 to confirm recording was added
    '''
    section_id = request.args(0,cast=int)
    youtube_id = xmlescape(request.args(1))
    section=db(db.course_section.id == section_id).select().first()
    if not section:
        raise HTTP(400,"Bad Request")
    #Some way to verify that the youtube_id is valid?
    #Yes- see https://groups.google.com/forum/#!topic/youtube-api-gdata/maM-h-zKPZc
    if (db((db.recording.youtube_id == youtube_id) & (db.recording.course_id == section_id)).isempty()):
        db.recording.insert(youtube_id=youtube_id,course_id=section_id)
        return 'added'
    else:
        #already have that recording for this section
        return 'already present'

@auth.requires_login()
def view():
    video_id = request.args(0,cast=int)
    video = db(db.recording.id==video_id).select().first()
    section_id = video.course_id
    if not is_user_student(section_id) and not is_user_teacher(section_id):
        redirect(URL('default','section', args=section_id))
    return dict(video=video)

@auth.requires_login()
def create():
    return dict()
