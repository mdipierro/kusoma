## Create the calendar menu.
if auth.is_logged_in():
    response.menu += [
        (T('Calendar'), False, '', [
                (T('My Calendar'), False, URL('calendar', 'index'), []),
                (T('Course Calendar'), False, URL('calendar', 'course_calendar'), []),
                (T('Create Event'), False, URL('calendar', 'create'), []),
                (T('Update Event'), False, URL('calendar', 'update'), []),
                (T('Delete Event'), False, URL('calendar', 'delete'), [])
        ])
    ]
