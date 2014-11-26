NE = IS_NOT_EMPTY()

"""
Basic information pertaining to
a chat session.
"""
db.define_table(
    'group_chat_session',
	Field('url'),
    Field('course_section', 'reference course_section', requires=NE),
    Field('start_time', 'datetime', default=request.now),
    Field('initiator', 'reference membership'),
)

"""
Individual chat settings for a user.
"""
db.define_table(
    'group_chat_user_settings',
    Field('user_id','reference membership', requires=NE),
    Field('mute_microphone', 'boolean'),
    Field('mute_web_camera', 'boolean')
)

"""
Connecting table relating users to chat sessions. This
links the users to their respective chat sessions.
"""
db.define_table(
    'group_chat_user_session',
    Field('session_id', 'reference group_chat_session', requires=NE),
    Field('user_id', 'reference membership', requires=NE)
)

def init_group_chat_session(course_section, user_id=auth.user_id, url=None):
    """
    Initiates a group chat session. Returns the group chat session id.
    """
    session_id = db.group_chat_session.insert(course_section=course_section,
											  url=url,
                                              initiator=user_id)
    db.group_chat_user_session.insert(session_id=session_id,
                                      user_id=user_id)
    db.commit()
    return session_id
	
def update_group_chat_session(session_id, url):
    """
	Updates the chat session with the url to join the session
	"""
    db(db.group_chat_session.id == session_id).update(url = url)
    db.commit()

def add_user_to_group_chat_session(group_chat_session_id, user_id=auth.user_id):
    """
    Adds the user to the already established chat session.
    """
    db.group_chat_user_session.insert(session_id=group_chat_session_id,
                                      user_id=user_id)
    db.commit()
	
def update_user_group_chat_settings(mute_microphone=False, mute_web_camera=False, user_id=auth.user_id):
    """
    Updates passed in user's group chat preferences if they exist, otherwise insert.
    """
    db.group_chat_user_settings.update_or_insert(user_id=user_id,
                                       mute_microphone=mute_microphone,
                                       mute_web_camera=mute_web_camera)
    db.commit()
    
def insert_user_group_chat_settings(mute_microphone=False, mute_web_camera=False, user_id=auth.user_id):
    """
    inserts passed in user's group chat preferences if they exist, otherwise insert.
    """
    db.group_chat_user_settings.insert(user_id=user_id,
                                       mute_microphone=mute_microphone,
                                       mute_web_camera=mute_web_camera)
    db.commit()
	
def update_user_setting_mic(mute_microphone, user_id=auth.user_id):
    """
	Updates the user settings with a true or false depending on if the user wants to use a mic
	"""
    db(db.group_chat_user_settings.user_id == user_id).update(mute_microphone = mute_microphone)
    db.commit()
	
def update_user_setting_cam(mute_web_camera, user_id=auth.user_id):
    """
	Updates the user settings with a true or false depending on if the user wants to use a camera
	"""
    db(db.group_chat_user_settings.user_id == user_id).update(mute_web_camera = mute_web_camera)
    db.commit()

def get_user_group_chat_settings(user_id=auth.user_id):
    """
    Retrieves a user's group chat settings.
    """
    data = db(db.group_chat_user_settings.user_id==user_id).select().first()
    return data

def user_group_chat_settings_exists(user_id=auth.user_id):
    """
    Checks to see if the user has settings in the table
    """
    return db(db.group_chat_user_settings.user_id==user_id).isempty()

def get_group_chat_sessions_for_user(user_id=auth.user_id):
    """
    Retrieves all of the chat sessions for the passed in user.
    """
    chatSessions = db(db.group_chat_user_session.user_id == user_id).select()
    toReturn = []
    for chatSession in chatSessions:
        toReturn.append({'session_info': (db(db.group_chat_session._id == chatSession.session_id).select())[0],
                         'members': db(db.group_chat_user_session.session_id == chatSession.session_id).select()})
    return toReturn
