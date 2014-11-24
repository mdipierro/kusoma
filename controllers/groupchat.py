@auth.requires_login()
def google_hangouts():
    courses = db(db.membership.auth_user == auth.user.id).select()
    response.files.insert(0, URL('static', 'css/chat.css'))
    return dict(courses=courses)


def hangouts_url_for_session():
    print "inside  hangouts_url_for_session"
    import gluon.contrib.simplejson as simplejson
    data = simplejson.loads(request.body.read())
    init_chat(data["sessionId"], data["hangoutsUrl"])
    return dict(data)

def group_chat():
    return dict()


# def chat_i_frame():
# return dict(sessions=get_group_chat_sessions_for_user())

@auth.requires_login()
def history():
    return dict(sessions=get_group_chat_sessions_for_user())


@auth.requires_login()
def history_session(session_id):
	return dict(messages=get_group_chat_messages_for_session(session_id))


@auth.requires_login()
def init_chat(course_section_id, url):
    return dict(session_id=init_group_chat_session(course_section_id, url))


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

