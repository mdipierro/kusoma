## Create the calendar menu.
response.menu += [
    (T('Calendar'), False, '', [
            (T('Create Event'), False, URL('calendar', 'create_event'), []),
            (T('My Calendar'), False, URL('calendar', 'user_calendar'), []),
            (T('Course Calendar'), False, URL('calendar', 'course_calendar'), [])
    ])
]
