NE = IS_NOT_EMPTY()

"""
Basic information pertainint to
a chat session.
"""
db.define_table(
    'group_chat_session',
    Field('title'),
    Field('start_time', 'datetime', default=request.now),
    Field('end_time', 'datetime'),
    Field('is_active', 'boolean', default=True),
    Field('initiator', 'reference auth_user'),
    Field('on_page')
)

"""
A single chat message that will be sent from
a user to a chat session (many users can receive a
single chat message).
"""
db.define_table(
    'group_chat_message',
    Field('chat_message'),
    Field('sender_id', 'reference auth_user', requires=NE),
    Field('to_session_id', 'reference group_chat_session', requires=NE),
    Field('time_sent', 'datetime', default=request.now)
)

"""
Individual chat settings for a user.
"""
db.define_table(
    'group_chat_user_settings',
    Field('auth_user','reference auth_user', requires=NE),
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
    Field('auth_user', 'reference auth_user', requires=NE)
)
