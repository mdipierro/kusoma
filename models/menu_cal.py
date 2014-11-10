## Create the calendar menu.
myevents = db(db.cal_event.owner_id == auth.user_id).select(db.cal_event.id, db.cal_event.title)
edit_events_sub_menu = []
delete_events_sub_menu = []

for event in myevents:
    edit_events_sub_menu.append((T(event.title), False, URL('calendar', 'edit', args=[event.id])))
    delete_events_sub_menu.append((T(event.title), False, URL('calendar', 'delete', args=[event.id])))

if auth.is_logged_in():
    response.menu += [
        (T('Calendar'), False, '', [
                (T('My Calendar'), False, URL('calendar', 'index'), []),
                (T('Course Calendar'), False, URL('calendar', 'course_calendar'), []),
                (T('Create Event'), False, URL('calendar', 'create'), []),
                (T('Update Event'), False, '', edit_events_sub_menu),
                (T('Delete Event'), False, '', delete_events_sub_menu)
        ])
    ]
