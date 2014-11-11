NE = IS_NOT_EMPTY()

"""
Basic information pertaining to
a chat session.
"""
db.define_table(
    'group_chat_session',
    Field('title'),
    Field('course_section', 'reference course_section', requires=NE),
    Field('start_time', 'datetime', default=request.now),
    Field('end_time', 'datetime'),
    Field('is_active', 'boolean', default=True),
    Field('initiator', 'reference membership'),
    Field('on_page')
)

"""
A single chat message that will be sent from
a user to a chat session (many users can receive a
single chat message).
"""
db.define_table(
    'group_chat_message',
    Field('chat_message', requires=NE),
    Field('sender_id', 'reference membership', requires=NE),
    Field('to_session_id', 'reference group_chat_session', requires=NE),
    Field('time_sent', 'datetime', default=request.now)
)

"""
Individual chat settings for a user.
"""
db.define_table(
    'group_chat_user_settings',
    Field('user_id','reference membership', requires=NE),
    Field('use_microphone', 'boolean'),
    Field('use_web_camera', 'boolean')
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

def init_group_chat_session(course_section_id, user_id=auth.user_id, title=None):
    """
    Initiates a group chat session. Returns the group chat session id.
    """
    session_id = db.group_chat_session.insert(course_section=course_section_id,
                                              initiator=user_id,
                                              title=title)
    db.group_chat_user_session.insert(session_id=session_id,
                                      user_id=user_id)
    db.commit()
    return session_id

def add_user_to_group_chat_session(group_chat_session_id, user_id=auth.user_id):
    """
    Adds the user to the already established chat session.
    """
    db.group_chat_user_session.insert(session_id=group_chat_session_id,
                                      user_id=user_id)
    db.commit()

def add_group_chat_message(message, group_chat_session_id, user_id=auth.user_id):
    """
    Associates the passed in message from the given sender to the passed
    in session.
    """
    db.group_chat_message.insert(chat_message=message,
                                 sender_id=user_id,
                                 to_session_id=group_chat_session_id)
    db.commit();

def add_user_group_chat_settings(user_id=request.now, use_microphone=False, use_web_camera=False):
    """
    Sets up passed in user's group chat preferences.
    """
    db.group_chat_user_settings.insert(user_id=user_id,
                                       use_microphone=use_microphone,
                                       use_web_camera=use_web_camera)
    db.commit();


def get_user_group_chat_settings(user_id=request.now):
    """
    Retrieves a user's group chat settings.
    """
    return db(db.group_chat_user_settings.user_id == user_id).select()

def get_group_chat_messages():
    """
    Retrieves all groups chat messages regardless of user
    """
    return db(db.group_chat_message).select()

def get_group_chat_messages_for_session(session_id):
    """
    Retrieve all messages for a chat session.
    """
    return db(db.group_chat_message.to_session_id == session_id).select()
