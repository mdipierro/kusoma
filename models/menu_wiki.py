response.menu += [
    (T('Wiki'), False, '', [
            (T('Show Wiki'), False, URL('wiki', 'wiki'), []),
            (T('Create Wiki'), False, URL('wiki', 'wikicreate'), []),
            (T('Search Wiki'), False, URL('wiki', 'wikisearch'), [])
    ])
]

