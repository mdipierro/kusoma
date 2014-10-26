## Create the calendar menu.
if auth.is_logged_in():
    response.menu += [
        (T('Calendar'), False, URL('calendar', 'index'), [
                (T('Create Event'), False, URL('calendar', 'create_event'), []),
                (T('My Calendar'), False, URL('calendar', 'user_calendar'), []),
                (T('Course Calendar'), False, URL('calendar', 'course_calendar'), [])
        ])
    ]
