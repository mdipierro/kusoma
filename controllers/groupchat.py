def group_chat():
    return dict()


@auth.requires_login()
def google_hangouts():
    """
    getting user data to pass to google_hangouts.html
    """
    memberships = db(db.membership.auth_user == auth.user.id).select()
    """
    if the user doesnt exist in the settings table, add them, then get their settings
    to return to google_hangouts.html
    """
    if user_group_chat_settings_exists():
        insert_user_group_chat_settings()
    user_settings = get_user_group_chat_settings()
    
    """
    get a list of the chat sessions
    """
    note_lists = []
    for membership in memberships:
        chat_sessions = db(db.group_chat_session.course_section == membership.course_section).select(
            db.group_chat_session.course_section, db.group_chat_session.url, db.group_chat_session.start_time)
        note_lists.append(chat_sessions)

    response.files.insert(0, URL('static', 'css/chat.css'))
    return dict(memberships=memberships, user_settings=user_settings,  ids=note_lists)


@auth.requires_login()
def hangouts_url_for_session():
    """
	This is called when the hangout starts up. The session id and url for the
	hangout are passed using JSON and then passed to update the existing row
	for the hangout. the user's settings are also loaded into the database.
	"""
    import gluon.contrib.simplejson as simplejson

    data = simplejson.loads(request.body.read())
    insert_new_hangout(data['course_section_id'], data['user_id'], data['hangoutUrl']);
    print "past insert_new_hangout"
    return dict(data)


@auth.requires_login()
def update_user_settings_microphone():
    """
	updates the user settings for the microphone
	"""
    import gluon.contrib.simplejson as simplejson

    data = simplejson.loads(request.body.read())
    update_user_setting_mic(data['muteMicrophone'])
    return dict(data)


@auth.requires_login()
def update_user_settings_camera():
    """
    updates the user settings for the camera
	"""
    import gluon.contrib.simplejson as simplejson

    data = simplejson.loads(request.body.read())
    update_user_setting_cam(data['muteCamera'])
    return dict(data)


@auth.requires_login()
def insert_new_hangout(course_section_id, user_id, hangout_url):
    """
	inserts a new hangout with the passed in course section
	"""
    return dict(session_id=init_group_chat_session(course_section_id, user_id, hangout_url))


@auth.requires_login()
def update_existing_hangout(session_id, url):
    """
	updates an existing hangout with the url to join that hangout
	"""
    update_group_chat_session(session_id, url)


@auth.requires_login()
def history():
    """
	returns the chat sessions the user belongs to
	"""
    return dict(sessions=get_group_chat_sessions_for_user())


@auth.requires_login()
def add_user_to_chat(session_id):
    """
    adds a user to the group chat
    """
    add_user_to_group_chat_session(session_id)
    return dict()
