def group_chat():
    return dict()

@auth.requires_login()
def google_hangouts():
    courses = db(db.membership.auth_user == auth.user.id).select()
    response.files.insert(0, URL('static', 'css/chat.css'))
    return dict(courses=courses)

@auth.requires_login()
def hangouts_url_for_session():
    import gluon.contrib.simplejson as simplejson
    data = simplejson.loads(request.body.read())
    update_existing_hangout(data["sessionId"], data["hangoutsUrl"])
    settings = get_user_group_chat_settings()
    update_user_group_chat_settings(settings.use_microphone, settings.use_camera)
    return dict(data)
	
@auth.requires_login()
def update_user_settings_microphone():
    import gluon.contrib.simplejson as simplejson
    data = simplejson.loads(request.body.read())
    update_user_setting_mic(data[muteMicrophone])
    return dict(data)

@auth.requires_login()
def update_user_settings_microphone():
    import gluon.contrib.simplejson as simplejson
    data = simplejson.loads(request.body.read())
    update_user_setting_cam(data[muteCamera])
    return dict(data)

@auth.requires_login()
def insert_new_hangout(course_section):
    return dict(session_id=init_group_chat_session(course_section))
	
@auth.requires_login()
def update_existing_hangout(session_id,  url):
    update_group_chat_session(session_id, url)

@auth.requires_login()
def history():
    return dict(sessions=get_group_chat_sessions_for_user())

@auth.requires_login()
def history_session(session_id):
	return dict(messages=get_group_chat_messages_for_session(session_id))

@auth.requires_login()
def add_user_to_chat(session_id):
	add_user_to_group_chat_session(session_id)
	return dict()

