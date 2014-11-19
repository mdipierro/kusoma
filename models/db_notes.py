#this is db file for notes
from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('note_main',
                #Field('note_id', unique=True, notnull=True),
                Field('course_id', 'reference course_section', required=IS_IN_DB(db, db.course_section.id, '%(name)s')),
                Field('create_on', 'datetime', default=request.now),
                Field('create_by', 'reference auth_user', default=auth.user_id),
                Field('version_id'))

db.define_table('note_tag',
                Field('note_id', 'reference note_main', notnull=True),
                Field('version_id', 'reference note_version', notnull=True),
                Field('tag'))

db.define_table('note_version',
                #Field('version_id', unique=True, notnull=True),
                Field('note_id', 'reference note_main', notnull=True),
                Field('modify_by', 'reference auth_user', default=auth.user_id),
                Field('modify_on', 'datetime', default=request.now),
                Field('title', type=str, notnull=True),
                Field('note_content', type=str, notnull=True))

db.define_table('note_discussion',
                Field('pid', default=0),
                Field('note_id', 'reference note_main', notnull=True),
                Field('create_on', 'datetime', default=request.now),
                Field('create_by', 'reference auth_user', default=auth.user_id),
                Field('post_content', type=str, notnull=True))

db.define_table('note_message',
                Field('user_id', 'reference auth_user', default=auth.user_id),
                Field('version_id', 'reference note_version'),
                Field('create_on', 'datetime', default=request.now),
                Field('has_read', type=bool, notnull=True))

db.define_table('note_user_note_relation',
                Field('note_id', 'reference note_main', notnull=True),
                Field('user_id', 'reference auth_user', default=auth.user_id),
                #two relations: unsubscribed 0, subscribed 1, and participated 2
                Field('relation', type=int, notnull=True))


class notedb:
    def __init__(self):
        pass

    #----------------------------------------------------------#
    #interface about notes
    #----------------------------------------------------------#
    def get_note_list(self):
        pass

    #include notes both subscribed and participated
    def get_my_note_list(self, user_id):
        pass

    def get_all_history_versions(self, note_id):
        pass

    #return notes ids that have at least one tag the same as designated
    def get_relevant_list(self, note_id):
        pass

    def get_note_content(self, note_id):
        pass

    def add_note_version(self, note_id, content):
        pass

    #----------------------------------------------------------#
    #interface about message
    #----------------------------------------------------------#
    def get_messages(self, user_id):
        pass

    def mark_message_read(self, message_id):
        pass

    def add_messages(self, version_id):
        pass

    #----------------------------------------------------------#
    #interface about discussion and post
    #----------------------------------------------------------#
    def get_discussions(self, note_id):
        pass

    def get_posts(self, discussion_id):
        pass

    def get_discussion_posts(self, note_id):
        pass

    def add_post(self, discussion_id, content):
        pass

    #----------------------------------------------------------#
    #interface about subscription
    #----------------------------------------------------------#
    def get_subscribed_notes(self, user_id):
        pass

    def subscribe_note(self, note_id, user_id):
        pass

    def unsubscribe_note(self, note_id, user_id):
        pass




def get_all_notes():
    return db().select(db.note_main.All)
