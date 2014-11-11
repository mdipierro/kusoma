## Create the calendar menu.
myevents = db(db.cal_event.owner_id == auth.user_id).select(db.cal_event.id,
                                                            db.cal_event.title,
                                                            db.cal_event.start_date)
update_events_sub_menu = []
delete_events_sub_menu = []

for event in myevents:
    menu_item = '%s (%s)' % (event.title, event.start_date.strftime(OUTPUT_DATE_FORMAT))
    update_events_sub_menu.append((T(menu_item), False, URL('calendar', 'update', args=[event.id])))
    delete_events_sub_menu.append((T(menu_item), False, URL('calendar', 'delete', args=[event.id])))

if auth.is_logged_in():
    response.menu += [
        (T('Calendar'), False, '', [
            (T('View Calendar'), False, URL('calendar', 'index'), []),
                (T('Course Calendar'), False, URL('calendar', 'course_calendar'), []),
                (T('Create Event'), False, URL('calendar', 'create'), []),
            (T('Update Event'), False, '', update_events_sub_menu),
            (T('Delete Event'), False, '', delete_events_sub_menu)
        ])
    ]
