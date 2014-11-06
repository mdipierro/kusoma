#this is db file for notes
from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('notes_main',
                Field('note_id', unique=True, notnull=True),
                Field('create_on', 'datetime', default=request.now),
                Field('course_id', 'reference course_section', required=IS_IN_DB(db, db.course_section.id, '%(name)s')),
                Field('tag'))

db.define_table('note_version',
                Field('version_id', unique=True, notnull=True),
                Field('note_id', 'reference notes_main', notnull=True),
                Field('modify_by', 'reference auth_user', default=auth.user_id),
                Field('modify_on', 'datetime', default=request.now),
                Field('note_content'))

db.define_table('note_favorite',
                Field('favorite_id', unique=True, notnull=True),
                Field('note_id', 'reference notes_main', notnull=True),
                Field('favorite_by', 'reference auth_user', default=auth.user_id))

db.define_table('note_chat',
                Field('session_id', unique=True, notnull=True),
                Field('note_id', 'reference notes_main', notnull=True),
                Field('create_on', 'datetime', default=request.now),
                Field('chat_by', 'reference auth_user', default=auth.user_id),
                Field('chat_content'))