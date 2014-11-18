# -*- coding: utf-8 -*-
# try something like
import time

def index():
    return get_note_list()

def notelist():
    return dict()

def mysubscriptions():
    return dict()

def notifications():
    return dict()


def notelist():
    return dict()

def mysubscriptions():
    return dict()

def notifications():
    return dict()

def notepage():
    return dict()

def noteeditpage():
    return dict()

def noteeditor():
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
    rows = db(query).select(db.note_version.note_id, db.note_version.title, db.note_main.creat_on, db.note_main.create_by, db.note_version.modify_on, db.note_version.modify_by, db.note_user_note_relation.user_id)
    return dict(rows=rows)

#include notes both subscribed and participated
def get_my_note_list(user_id):
    query = (db.note_main.id == db.note_version.note_id
            )&(db.note_user_note_relation.note_id == user_id
            )&(db.note_main.id == db.note_user_note_relation.note_id
            )&(db.db.note_version.modify_on == db(db.note_main.id == db.note_version.note_id).select(max(db.note_version.modify_on)))
    rows = db(query).select(db.note_version.title, db.note_main.creat_on, db.note_main.create_by, db.db.note_version.modify_on, db.db.note_version.modify_by, db.note_user_note_relation.user_id)
    return dict(rows=rows)

def search_note_list(search_content):
    search_content = "%" + search_content.upper().strip() + "%"
    query = (db.note_main.id == db.note_version.note_id
            )&(db.note_main.id == db.note_user_note_relation.note_id
            )&(db.note_version.note_content.upper().like(search_content)
            )&(db.db.note_version.modify_on == db(db.note_main.id == db.note_version.note_id).select(max(db.note_version.modify_on)))
    rows = db(query).select(db.note_version.note_id, db.note_version.title, db.note_main.creat_on, db.note_main.create_by, db.note_version.modify_on, db.note_version.modify_by, db.note_user_note_relation.user_id)
    return dict(rows=rows)

def get_all_history_versions(note_id):
    query = (db.note_version.note_id == note_id)
    rows = db(query).select(db.note_version.title, db.note_version.modify_by, db.note_version.modify_on)
    return dict(rows=rows)

#return notes ids that have at least one tag the same as designated
def get_relevant_list(note_id):
    query_note_id = db(db.note_tag.tag.upper().strip() == (db(db.note_tag.note_id == note_id).select(db.note_tag.tag)).upper().strip())
    
    query_relevant_note = (db.note_main.id == db.note_version.note_id
            )&(db.note_main.id in (db(query_note_id).select(db.note_tag.note_id))
            )&(db.db.note_version.modify_on == db(db.note_main.id == db.note_version.note_id).select(max(db.note_version.modify_on)))
            
    rows = db(query_relevant_note).select(db.note_version.title)
    return dict(rows=rows)

def get_note_content(note_id):
    query = (db.note_main.id == db.note_version.note_id
            )&(db.note_main.id == note_id
            )&(db.db.note_version.modify_on == db(db.note_main.id == db.note_version.note_id).select(max(db.note_version.modify_on)))
    rows = db(query).select(db.note_version.note_content)
    return dict(rows=rows)

def add_new_note(course_id, user_id):
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
def get_messages(user_id):
    query = (db.note_message.id == user_id) & (db.note_message.version_id == db.note_version.id)
    rows = db(query).select(db.note_version.note_id, db.note_version.title, db.note_version.modify_by, db.note_version.modify_on, db.note_message.has_read)
    return dict(rows=rows)

def mark_message_read(message_id):
    db(db.note_message.id == message_id).update(has_read = True)
    db.commit()


def add_messages(user_id, version_id):
    db.note_message.insert(user_id = user_id, version_id = version_id, create_on = time.time(), has_read = False)
    db.commit()


#----------------------------------------------------------#
#interface about discussion and post
#----------------------------------------------------------#
def get_discussions(note_id):
    rows_from = db(db.note_discussion).select()
    discussions = []
    for row in rows_from:
        if row.note_id == note_id:
            discussion = {'id': row.id, 'pid': row.pid, 'create_on': row.create_on, 'user': row.user_id, 'content': row.post_content}
            discussions.append(discussion)
    return dict(rows=discussions)


def add_discussion(note_id, pid, content):
    db.note_discussion.update_or_insert(note_id=note_id, pid=pid, create_on=request.now, create_by=auth.user_id, post_content=content)
    db.commit()


#----------------------------------------------------------#
#interface about subscription
#----------------------------------------------------------#
def get_subscribed_notes(user_id):
    rows_from = db(db.note_user_note_relation).select()
    notes_list = []
    for row in rows_from:
        if row.user_id == user_id and row.relation is True:
            notes_list.append(row.note_id)
    return dict(rows=notes_list)


def subscribe_note(note_id, user_id):
    db.note_user_not_relation.update_or_insert(note_id=note_id, users_id=user_id, relation=True)
    db.commit()


def unsubscribe_note(note_id, user_id):
    db.note_user_not_relation.update_or_insert(note_id=note_id, users_id=user_id, relation=False)
    db.commit()
