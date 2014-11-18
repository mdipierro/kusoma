## Create the calendar menu.
if auth.is_logged_in():
    events_menu_items = []
    events_menu_items.append((T('My Calendar'), False, URL('calendar', 'my_calendar'), []))

    if CAN_MANAGE_EVENTS:
        events_menu_items.append((T('Create Event'), False, URL('calendar', 'create'), []))
        events_menu_items.append((T('Manage Events'), False, URL('calendar', 'manage'), []))

    response.menu += [
        (T('Calendar'), False, '', events_menu_items)
    ]
