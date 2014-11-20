# coding: utf8
#This is the controller for the class recordings module of LMS299

#HMAC key to use for signing the hangouts app callback URL
#TODO: This should be randomly generated once at server startup and stored somewhere(?)
#so that it is not publicly accessible.
API_SIGN_KEY = '46bhvw1ymnV2178GXYOrbqKfkfyYfM7RrDoqffq9v+N5'

@auth.requires_login()
def index():
    """
    Show the list of recordings for a section
    arg1 - the section_id
    """
    sections = my_sections()

    return dict(sections=sections)

@auth.requires_login()
def section():
    """
    Show the list of recordings for a section
    arg1 - the section_id
    """
    section_id = request.args(0,cast=int)
    section = db.course_section(section_id) or redirect(URL('default','index'))
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
def edit():
    """
    Edit an entry in the recording database.
    arg1 - the recording id
    """
    # Get video id if provided
    video_id = request.args(0,cast=int)
    video = db.recording(video_id) or redirect(URL('default','index'))

    section_id = video.course_id
    add_section_menu(section_id)

    # Test if user is the teacher or video recorder
    # If not then redirect to course page
    if is_user_teacher(section_id):
        fields = ['name', 'is_class', ]
        able_to_delete = True
    elif video.recorder==auth.user_id:
        fields = ['name']
        able_to_delete = True
    else:
        redirect(URL('section', args=section_id))

    # Create a form based on recording db
    form = SQLFORM(db.recording, video, fields=fields, deletable=able_to_delete)
    form.add_button('Back', URL('section', args=section_id))

    # If form is accepted then update recording db and send to course page
    if form.process().accepted:
        session.flash = 'Form accepted'
        redirect(URL('section', args=section_id))
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
    section = db.course_section(section_id) or redirect(URL('default','index'))
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


    ###################################
    # Build form for existing recording
    ###################################

    fields_existing = [Field('youtube_link', label=T('Youtube URL'))]
    if is_user_teacher(section_id):
        fields_existing.append(Field('is_class', 'boolean', label=T('This is an official class recording'), default=True))

    form_existing = SQLFORM.factory(*fields_existing)

    def check_youtube(form):
        """
        Parse the given form.vars.youtube_link to extract the youtube ID, then
        check that Youtube ID is valid.
        If valid, then form_existing.vars.youtube_id will contain the youtube ID
        and form_existing.vars.youtube_title will contain the Youtube title.
        If invalid, form.errors.youtube will contain an error message.
        """
        try:
            form.vars.youtube_id = get_youtube_id(form.vars.youtube_link)
            form.vars.youtube_title = get_youtube_title(form.vars.youtube_id)
        except:
            form.errors.youtube = 'Invalid Youtube URL'

    #If form is accepted then write to recording db and send back to course page
    if form_existing.process(onvalidation=check_youtube).accepted:
        if is_user_teacher(section_id):
            set_is_class = form_existing.vars.is_class
        else:
            set_is_class = False

        db.recording.course_id.writable=True
        db.recording.insert(
            name=form_existing.vars.youtube_title,
            youtube_id=form_existing.vars.youtube_id,
            course_id=section_id,
            is_class=set_is_class)
        db.recording.course_id.writable=False

        session.flash = 'Added recording'
        redirect(URL('section', args=section_id))
    elif form_existing.errors:
        if form_existing.errors.youtube:
            response.flash = form_existing.errors.youtube
        else:
            response.flash = 'Form has errors'

    return dict(form_new=form_new, form_existing=form_existing, section=section)

@auth.requires_login()
def new_recording():
    """
    This is an ajax callback from the create view. It will load the hangouts button
    in place of the 'Start a new hangout button'.
    """
    section_id = request.args(0,cast=int)

    id = db.recording.insert(course_id=section_id)
    return LOAD('recordings', 'start.load', args=id, ajax=True)

@auth.requires_login()
def start():
    """
    This loads the Hangouts button
    """
    video_id = request.args(0,cast=int)
    video = db.recording(video_id) or redirect(URL('default','index'))

    section_id = video.course_id
    add_section_menu(section_id)

    users = dict()
    start = False

    if not video.youtube_id:
        start = True
    users = users_in_section(9, [STUDENT,TEACHER])
    callback_url=URL('recordings', 'api', args=['recording', video.id], vars=request.get_vars, host=True, hmac_key=API_SIGN_KEY)

    return dict(start=start, users=users, callback_url=callback_url)

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
    
    #Verify URL signature using HMAC key
    if not URL.verify(request, hmac_key=API_SIGN_KEY): raise HTTP (403)
    
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
                return db(db.recording.id == args[1]).validate_and_update(youtube_id=vars['youtube_id'], name=get_youtube_title(vars['youtube_id']))
        return dict()

    def DELETE(*args,**vars):
        return dict()

    def OPTIONS(*args,**vars):
        return dict()
    return locals()

#Leaving this here as another example of how the RESTFUL API might be written
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

def get_youtube_title(video_id):
    """
    Use to get the Youtube video title using the video id
    raises JSONDecodeError if video_id is not a valid Youtube ID
    To check for this error, you must "from simplejson import JSONDecodeError"
    """
    import urllib
    import simplejson

    link = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % video_id
    json = simplejson.load(urllib.urlopen(link))
    title = json['entry']['title']['$t']
    return title

def get_youtube_id(link):
    """
    Use to get Youtube id using the link
    """
    #TODO - this should also parse URL's of the form http://youtu.be/dQw4w9WgXcQ, and other patterns, too?
    import urlparse
    url = urlparse.urlparse(link)
    query = urlparse.parse_qs(url.query)
    id = query["v"][0]
    return id
