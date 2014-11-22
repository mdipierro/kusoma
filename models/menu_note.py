response.menu += [
    (T('Notes'), False, URL('notes', '#'), [
        (T('All Notes'), False, URL('notes', 'index'), []),
        (T('My Subscription'), False, URL('notes', 'mysubscriptions'), []),
        (T('Notifications'), False, URL('notes', 'notifications'), [])
    ])
]
