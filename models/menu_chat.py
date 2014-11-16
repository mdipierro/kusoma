# Navigational menu for Group Chat
# response.menu.append(('Chat', False, None, [
#     ('History', False, URL('groupchat', 'history'))
#     ('Google Hangouts', False, URL('groupchat', 'google_hangouts'))
# ]))


response.menu += [
    (T('Chat'), False, '', [
        (T('History'),      False, URL('groupchat', 'history'),         []),
        ('Google Hangouts', False, URL('groupchat', 'google_hangouts'), [])
    ])
]




