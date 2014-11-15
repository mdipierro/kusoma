## Create the calendar menu.
if auth.is_logged_in():
    response.menu += [
        (T('Calendar'), False, URL('calendar', 'index'), [
                (T('My Calendar'), False, URL('calendar', 'my_calendar'), []),
                (T('Create Event'), False, URL('calendar', 'create'), []),
                (T('Manage Events'), False, URL('calendar', 'manage'), []),
        ])
    ]
