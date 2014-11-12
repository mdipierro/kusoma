# -*- coding: utf-8 -*-
# try something like
import time

def index():
    return dict()
def notelist():
    return dict()
def mysubscriptions():
    return dict()
def notifications():
    return dict()

#def get_all_notes():
#    return db().select(db.note_main.All)

#def add_note(course_id, tag):
#    db.notes_main.insert(course_id = course_id, tag = tag, create_on = time.time())
#    db.commit()
    
#----------------------------------------------------------#
#interface about notes
#----------------------------------------------------------#
def get_note_list():
    query = (db.note_main.id == db.note_version.note_id
            )&(db.note_main.id == db.note_user_note_relation.note_id
            )&(db.db.note_version.modify_on == db(db.note_main.id == db.note_version.note_id).select(max(db.note_version.modify_on)))

    return db(query).select(db.note_version.title, db.note_main.creat_on, db.note_main.create_by, db.db.note_version.modify_on, db.db.note_version.modify_by, db.note_user_note_relation.user_id)

#include notes both subscribed and participated
def get_my_note_list(user_id):
    query = (db.note_main.id == db.note_version.note_id
            )&(db.note_user_note_relation.note_id == user_id
            )&(db.note_main.id == db.note_user_note_relation.note_id
            )&(db.db.note_version.modify_on == db(db.note_main.id == db.note_version.note_id).select(max(db.note_version.modify_on)))
    return db(query).select(db.note_version.title, db.note_main.creat_on, db.note_main.create_by, db.db.note_version.modify_on, db.db.note_version.modify_by, db.note_user_note_relation.user_id)

def get_all_history_versions(note_id):
    query = (db.note_version.note_id == note_id)
    return db(query).select(db.note_version.title, db.note_version.modify_by, db.note_version.modify_on)

#return notes ids that have at least one tag the same as designated
def get_relevant_list(self, note_id):
    pass

def get_note_content(self, note_id):
    pass
def add_new_note():
    #get course_id user_id from request?
    db.notes_version.insert(course_id = course_id, create_by = user_id, create_on = time.time())
    db.commit()
    
def add_note_version(note_id, content):
    #get user_id from request?
    db.notes_version.insert(note_id = note_id, modify_by = user_id, modify_on = time.time(), title = title, note_content = content)
    db.commit()
    
def add_tag(note_id, tag):
    db.note_tag.update_or_insert(note_id = note_id, tag = tag)
    db.commit()
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
