@auth.requires_login()
def history():
    return dict(sessions=get_group_chat_sessions_for_user())

@auth.requires_login()
def history_session(session_id):
	return dict(messages=get_group_chat_messages_for_session(session_id))

@auth.requires_login()
def init_chat(course_section_id, title):
	return dict(session_id=init_group_chat_session(course_section_id, title))

@auth.requires_login()
def add_user_to_chat(session_id):
	add_user_to_group_chat_session(session_id)
	return dict()
	
@auth.requires_login()
def add_message(message, session_id):
	add_group_chat_message(message, session_id())
	return dict()
	
@auth.requires_login()
def add_user_settings_default():
	add_user_group_chat_settings()
	return dict()
	
@auth.requires_login()
def add_user_settings(use_microphone, use_camera):
	add_user_group_chat_settings(use_microphone, use_camera)
	return dict()
	
@auth.requires_login()
def update_user_settings(use_microphone, use_camera):
	update_user_group_chat_settings(use_microphone, use_camera)
	return dict()
	
@auth.requires_login()
def get_user_settings():
	return dict(settings=get_user_group_chat_settings())

