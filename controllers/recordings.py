# coding: utf8
#This is the controller for the class recordings module of LMS299

@auth.requires_login()
def index():
    section_id = request.args(0,cast=int)

    add_section_menu(section_id)

    section=db(db.course_section.id == section_id).select().first()
    if not section: redirect(URL('default','index'))

    videos = db(db.recording.course_id==section_id).select()
    if is_user_student(section_id):
        is_teacher=False
    elif is_user_teacher(section_id):
        is_teacher=True
    else:
        redirect(URL('default','section', args=section_id))
        
    #Here's a possible way of encoding callback URL and section_id for start_data to hangouts app
    #to decode in javascript: https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
    import urllib
    start_data=urllib.urlencode(dict(callback=URL('update_recording', scheme=True, host=True), section_id=section_id))
    
    return dict(section=section, videos=videos, is_teacher=is_teacher, start_data=start_data)

#@auth.requires_login()   #John disabled for now, see below
def update_recording():
    '''
    This is a callback function to register a new recording.
    request.args[0]= The section_id
    request.args[1]= The youtube_id of the new recording

    Test example: Adds a recording to course_section 2
    Visit lms299/recordings/add_recording/2/aKdV5FvXLuI
    Then visit lms299/recordings/index/2 to confirm recording was added
    '''
    
    '''
    The following line is needed so that the Hangouts app is able to access this function.
    Without it, the hangout javascript console will have an error:
    
    XMLHttpRequest cannot load ... No 'Access-Control-Allow-Origin' header is present
    on the requested resource. Origin ... is therefore not allowed access.
    
    Note also, the same error appears when this function requires login because for
    some reason, the hangout window is not sending the session cookie to the web2py
    server, even when I am logged into the web2py server.
    '''
    response.headers['Access-Control-Allow-Origin'] = '*'
    
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
def edit():
    video_id = request.args(0,cast=int)

    if video_id:
        video = db(db.recording.id==video_id).select().first()
        courseId = video.course_id
        if (not video or not is_user_teacher(video.course_id)):
            redirect(URL('index', args=video.course_id))

    form = SQLFORM(db.recording, video)
    form.add_button('Back', URL('index', args=courseId))

    if form.process().accepted:
        response.flash = 'Form accepted'
        redirect(URL('index', args=courseId))
    elif form.errors:
        response.flash = 'Form has errors'
    return dict(form=form)

@auth.requires_login()
def create():
    # Get section id if provided
    section_id = request.args(0,cast=int)

    # Test if current user is teacher or student for class
    # if teacher, is_class field can be set to true
    if is_user_teacher(section_id):
        fields = ['name', 'is_class', ]
    elif is_user_student(section_id):
        fields = ['name']
    else:
        redirect(URL('section',args=section_id))

    start = False

    db.recording.course_id.default = section_id

    form = SQLFORM(db.recording, fields=fields)

    # If form is accepted we show start a hangout button
    # TODO add condition to verify hangout has not yet been started
    if form.process().accepted:
        start = True
        redirect(URL('start', args=(form.vars.id)))

    if start:
        users = users_in_section(section_id, roles=[STUDENT, TEACHER])
    else:
        users = dict()

    return dict(form=form, start=start)

@auth.requires_login
def start():
    video_id = request.args(0,cast=int)
    video = db(db.recording.id==video_id).select().first()

    users = dict()
    start = False

    if video:
        if not video.youtube_id:
            start = True
            users = users_in_section(video.course_id, roles=[STUDENT,TEACHER])



    return dict(video=video, start=start, users=users)

@request.restful()
def api():
    if request.env.http_origin:
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'PUT'
        response.headers['Access-Control-Allow-Headers'] = request.env.http_access_control_request_headers
        response.headers['Access-Control-Max-Age'] = 86400
    def GET(*args,**vars):
        return dict()
    def POST(*args,**vars):
        return dict()
    def PUT(*args,**vars):
        if args[0] == 'recording':
            if args[1]:
                return db(db.recording.id == args[1]).validate_and_update(**vars)
        return dict()

    def DELETE(*args,**vars):
        return dict()

    def OPTIONS(*args,**vars):
        return dict()
    return locals()

# def api():
#     from gluon.contrib.hypermedia import Collection
#     rules = {
#         'recording': {
#             'GET':{'query':None,'fields':['id','name']},
#             'POST':{},
#             'PUT':{'query':None,'fields':['name','youtube_id']},
#             'DELETE':{}
#         },
#         #'recording': {'GET':{},'POST':{},'PUT':{},'DELETE':{}}
#         }
#     return Collection(db).process(request,response,rules)
