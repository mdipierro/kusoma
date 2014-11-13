@auth.requires_login()
def history():
    return dict(group_chats=get_group_chat_messages())

@auth.requires_login()
def history_session(session_id):
	return dict(messages=get_group_chat_messages_for_session(session_id)))

@auth.requires_login()
def init_chat(course_section_id, title)
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
def add_user_settings(use_microphone, use_camera):
	add_user_group_chat_settings(use_microphone, use_camera)
	return dict()
	
@auth.requires_login()
def get_user_settings()
	return(settings=get_user_group_chat_settings())
	


	
