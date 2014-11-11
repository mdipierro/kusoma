
response.menu += [
    (T('Themes'), False, '', [
        (T('Choose Theme'), False, URL('themes', 'index'), []),
        (T('Set a Course Theme'), False, URL('themes', 'course_themes'), [])
    ])
]
