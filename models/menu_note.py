response.menu += [
    (T('Notes'), False, '', [
        (T('Search'), False, URL('notes', 'notelist'), []),
        (T('My Subscription'), False, URL('notes', 'mysubscriptions'), []),
        (T('Notifications'), False, URL('notes', 'notifications'), [])
    ])
]
