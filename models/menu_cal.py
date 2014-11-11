## Create the calendar menu.

## Create our list of menu items programmatically
## so we can display items based on permissions.
events_menu_items = []

## Public events - viewable witout logging in.
events_menu_items.append((T('View Calendar'), False, URL('calendar', 'index'), []))

if auth.is_logged_in():
    events_menu_items.append((T('Course Calendar'), False, URL('calendar', 'course_calendar'), []))

    if CAN_MANAGE_EVENTS:
        update_events_sub_menu = []
        delete_events_sub_menu = []
        myevents = db(db.cal_event.owner_id == auth.user_id).select(db.cal_event.id,
                                                                    db.cal_event.title,
                                                                    db.cal_event.start_date)

        if myevents:
            for event in myevents:
                menu_item = '%s (%s)' % (event.title, event.start_date.strftime(OUTPUT_DATE_FORMAT))
                update_events_sub_menu.append((T(menu_item), False, URL('calendar', 'update', args=[event.id])))
                delete_events_sub_menu.append((T(menu_item), False, URL('calendar', 'delete', args=[event.id])))

            events_menu_items.append((T('Create Event'), False, URL('calendar', 'create'), []))
            events_menu_items.append((T('Update Event'), False, '', update_events_sub_menu))
            events_menu_items.append((T('Delete Event'), False, '', delete_events_sub_menu))

response.menu += [(T('Events'), False, '', events_menu_items)]
