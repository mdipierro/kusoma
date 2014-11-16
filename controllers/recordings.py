# coding: utf8
#This is the controller for the class recordings module of LMS299

@auth.requires_login()
def index():
    """
    Show the list of recordings for a section
    arg1 - the section_id
    """
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
    if not video: redirect(URL('default','index'))
        
    section_id = video.course_id
    if not is_user_student(section_id) and not is_user_teacher(section_id):
        redirect(URL('default','section', args=section_id))

    add_section_menu(section_id)
    
    return dict(video=video)

@auth.requires_login()
def edit():
    """
    Edit an entry in the recording database.
    arg1 - the recording id
    """
    
	# Get video id if provided
    video_id = request.args(0,cast=int)
    video = db(db.recording.id==video_id).select().first()
    if not video: redirect(URL('default','index'))

    section_id = video.course_id
    add_section_menu(section_id)

	# Test if user is the teacher
	# If not then redirect to course page
    if not is_user_teacher(video.course_id):
        redirect(URL('index', args=video.course_id))

	# Create a form based on recording db
    form = SQLFORM(db.recording, video, deletable = True)
    form.add_button('Back', URL('index', args=video.course_id))

	# If form is accepted then update recording db and send to course page
    if form.process().accepted:
        response.flash = 'Form accepted'
        redirect(URL('index', args=courseId))
    elif form.errors:
        response.flash = 'Form has errors'
    return dict(form=form)

@auth.requires_login()
def create():
    """
    Display two forms: one to create a new hangout on air and another to add an already
    existing youtube video to the database of recordings for the section.
    arg1 - the section_id of the section for which the recording should be added
    """
    # Get section id if provided
    section_id = request.args(0,cast=int)
    section=db(db.course_section.id == section_id).select().first()
    if not section: redirect(URL('default','index'))
        
    add_section_menu(section_id)

    ###################################
    # Build form for new recording
    ###################################
    
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

    form_new = SQLFORM(db.recording, fields=fields)

    # If form is accepted we show start a hangout button
    # TODO add condition to verify hangout has not yet been started
    if form_new.process().accepted:
        start = True
        redirect(URL('start', args=(form_new.vars.id)))

    if start:
        users = users_in_section(section_id, roles=[STUDENT, TEACHER])
    else:
        users = dict()

        
    ###################################
    # Build form for existing recording
    ###################################
    
    ##TODO - Don't redirect here - just don't show is_class checkbox if not a teacher
    # Test if teacher, if not send to course page
    if not is_user_teacher(section_id):
        redirect(URL('index',args=section_id))

	# Create form based on recording db
	# Additional link field, and a hidden course field so that user can not change it
    #TODO - Change field order to put youtube id and link next to each other
    #TODO - Make Recorder and date fields not readable, not writable - default to current user and time
    fields = [field for field in db.recording]
    fields += [Field('youtube_link', label=T('Youtube Link')), Field('course_id', type='hidden')]
    form_existing = SQLFORM.factory(*fields)
    form_existing.add_button('Back', URL('index', args=section_id))
    form_existing.vars.course_id = section_id

	# Test if there is a Youtube Link
	# If there is then get the Youtube ID to store in db
    def check_youtube(form):
        if not form_existing.vars.youtube_link and not form_existing.vars.youtube_id:
            form_existing.errors.youtube = 'Fill in a Youtube Link or ID'
        elif form_existing.vars.youtube_link and not form_existing.vars.youtube_id:
            form_existing.vars.youtube_id = get_youtube_id(form_existing.vars.youtube_link)

	#If form is accepted then write to recording db and send back to course page
    if form_existing.process(onvalidation=check_youtube).accepted:
        db.recording.course_id.writable=True
        db.recording.insert(**db.recording._filter_fields(form_existing.vars))
        db.recording.course_id.writable=False

        response.flash = 'Form accepted'
        redirect(URL('index', args=section_id))
    elif form_existing.errors:
        if form_existing.errors.youtube:
            response.flash = form_existing.errors.youtube
        else:
            response.flash = 'Form has errors'

    return dict(form_new=form_new, form_existing=form_existing, section=section)

#Jeremy would like this to be integrated with create() such that the start-a-hangout button will only appear
#when the form has been filled out.
@auth.requires_login()
def start():
    video_id = request.args(0,cast=int)
    video = db(db.recording.id==video_id).select().first()
    if not video: redirect(URL('default','index'))

    section_id = video.course_id
    add_section_menu(section_id)

    users = dict()
    start = False

    if not video.youtube_id:
        start = True
        users = users_in_section(9, [STUDENT,TEACHER])

    return dict(video=video, start=start, users=users)

@request.restful()
def api():
    """
    API for posting a new recording from the Hangouts app.
    It is assumed that an entry was already initialized in the database with all the fields populated
    except the youtube_id. The URL to this API should be pass to the hangouts app as its start data.
    The URL should have:
        args[0] = 'recording'
        args[1] = the recording id that should be updated.
    When the hangouts app starts and obtains its youtube_id, it should callback to this function with
    the youtube_id as a variable. The vars for the request will be used to update the database entry
    for the recording id.
    """
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

#Use to get the Youtube video title using the video id
def get_youtube_title(video_id):
    import urllib
    import simplejson

    link = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % video_id
    json = simplejson.load(urllib.urlopen(link))
    title = json['entry']['title']['$t']
    return title
	
#Use to get Youtube id using the link
def get_youtube_id(link):
	import urlparse
	
	url = urlparse.urlparse(link)
	query = urlparse.parse_qs(url.query)
	id = query["v"][0]
	return id
