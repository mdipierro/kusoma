# -*- coding: utf-8 -*-
# try something like
import time
import json

import logging
logger = logging.getLogger("web2py.app.lms299")
logger.setLevel(logging.DEBUG)

def index():
    return get_note_list('')

@auth.requires_login()
def mysubscriptions():
    rows = db(db.note_user_note_relation.user_id == auth.user_id and db.note_user_note_relation.relation == True).select()
    
    note_lists = []
    for row in rows:
        note_list = get_note_by_id(row.note_id)["notes"]
        for one_row in note_list:
            one_row["user_id"] = auth.user_id
            note_lists.append(one_row)
    return dict(notes=note_lists)

@auth.requires_login()
def unsubscribe_note_request():
    if request.vars["note_id"] and request.vars["user_id"]:
        unsubscribe_note(request.vars["note_id"], request.vars["user_id"])
    redirect(URL('mysubscriptions'))

@auth.requires_login()
def notifications():
    return get_messages(auth.user_id)

@auth.requires_login()
def mark_message_read_request():
    message_id = request.vars["message_id"]
    vid = request.vars["vid"]
    
    if message_id:
        mark_message_read(message_id)
    redirect(URL('notepage', args=[''], vars=dict(vid=vid)))

@auth.requires_login()
def mynotes():
    return get_my_note_list(auth.user_id)

def notepage():
    vid = request.vars.vid
    note = get_note_by_vid(vid)
    return note
@auth.requires_login()
def noteeditpage():
    return dict()

@auth.requires_login()
def noteeditor():
    course_info = db().select(db.course.id, db.course.code)

    if 'vid' in request.vars:
        vid = request.vars.vid
        result = dict( get_note_by_vid(vid),courseList=course_info)
        logger.debug(result)
    else:
        result = dict(courseList=course_info)
    return result

def getNotePost():
    uid = auth.user_id
    cid = request.vars.CourseId
    title = request.vars.Title
    tag = request.vars['Tag[]']
    content = request.vars.Content
    action = request.vars.Action
    try:
        logger.debug(action)
        if action == 'add':
            nid = add_new_note(cid, uid)
        elif action == 'update':
            nid = request.vars.NoteId
        logger.debug(nid)
        vid = add_note_version(nid, uid,title, content)
        add_tag(vid, tag)
    except Exception, e:
        logger.error('error:%s' % e)
        
    return dict(VersionId='vid')

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


#include notes both subscribed and participated
def get_my_note_list(user_id):
    query = (db.note_main.id == db.note_version.note_id
            )&(db.note_user_note_relation.user_id == user_id
            )&(db.note_main.version_id == db.note_version.id
            )&(db.note_user_note_relation.relation == True
            )&(db.note_main.id == db.note_user_note_relation.note_id)
    rows = db(query).select()
    
    note_lists = []
    for row in rows:
        create_by = (db(db.auth_user.id == row.note_main.create_by).select().first()).first_name + ' ' + (db(db.auth_user.id == row.note_main.create_by).select().first()).last_name
        modify_by = (db(db.auth_user.id == row.note_version.modify_by).select().first()).first_name + ' ' + (db(db.auth_user.id == row.note_version.modify_by).select().first()).last_name
        note_list = {'note_id': row.note_main.id, 'version_id': row.note_main.version_id, 'title': row.note_version.title, 'create_by': create_by, 'create_on': row.note_main.create_on, 'modify_by': modify_by, 'modify_on': row.note_version.modify_on}
        note_lists.append(note_list)
        
    return dict(notes=note_lists)
    
def get_note_list(search_content):
    query = (db.note_main.id == db.note_version.note_id)&(db.note_version.note_content.upper().contains(search_content.upper().strip()))&(db.note_main.version_id == db.note_version.id)&(db.note_main.course_id == db.course.id)
    rows = db(query).select()
    
    note_lists = []
    for row in rows:
        create_by = (db(db.auth_user.id == row.note_main.create_by).select().first()).first_name + ' ' + (db(db.auth_user.id == row.note_main.create_by).select().first()).last_name
        modify_by = (db(db.auth_user.id == row.note_version.modify_by).select().first()).first_name + ' ' + (db(db.auth_user.id == row.note_version.modify_by).select().first()).last_name
        note_list = {'note_id': row.note_main.id, 'version_id': row.note_main.version_id, 'title': row.note_version.title, 'create_by': create_by, 'create_on': row.note_main.create_on, 'modify_by': modify_by, 'modify_on': row.note_version.modify_on, 'course_code':row.course.code}
        note_lists.append(note_list)
        
    return dict(notes=note_lists)     

def get_note_by_vid(vid):
    query = (db.note_version.id == vid)&(db.note_version.id == db.note_tag.version_id)&(db.note_main.version_id ==db.note_version.id)
    rows = db(query).select(db.note_version.ALL,db.note_main.course_id,db.note_tag.tag)

    return dict(note=rows[0]) 

def get_note_by_id(note_id):
    query = (db.note_main.id == note_id)&(db.note_main.id == db.note_version.note_id)&(db.note_main.version_id == db.note_version.id)
    rows = db(query).select()
    
    note_lists = []
    for row in rows:
        create_by = (db(db.auth_user.id == row.note_main.create_by).select().first()).first_name + ' ' + (db(db.auth_user.id == row.note_main.create_by).select().first()).last_name
        modify_by = (db(db.auth_user.id == row.note_version.modify_by).select().first()).first_name + ' ' + (db(db.auth_user.id == row.note_version.modify_by).select().first()).last_name
        note_list = {'note_id': row.note_main.id, 'version_id': row.note_main.version_id, 'title': row.note_version.title, 'create_by': create_by, 'create_on': row.note_main.create_on, 'modify_by': modify_by, 'modify_on': row.note_version.modify_on}
        note_lists.append(note_list)
        
    return dict(notes=note_lists) 

def get_all_history_versions(note_id):
    query = (db.note_version.note_id == note_id)
    rows = db(query).select(db.note_version.title, db.note_version.modify_by, db.note_version.modify_on)
    return dict(rows=rows)

#return notes ids that have at least one tag the same as designated
def get_relevant_list(note_id):
    query_note_id = db(db.note_tag.tag.upper().strip() == (db(db.note_tag.note_id == note_id).select(db.note_tag.tag)).upper().strip())
    
    query_relevant_note = (db.note_main.id == db.note_version.note_id
            )&((db(query_note_id).select(db.note_tag.note_id)).contains(db.note_main.id)
            )&(db.note_version.modify_on == db(db.note_main.id == db.note_version.note_id).select(db.note_version.modify_on.max()))
            
    rows = db(query_relevant_note).select(db.note_version.title)
    return dict(rows=rows)

def get_note_content(note_id):
    query = (db.note_main.id == db.note_version.note_id
            )&(db.note_main.id == note_id
            )&(db.note_version.modify_on == db(db.note_main.id == db.note_version.note_id).select(db.note_version.modify_on.max()))
    rows = db(query).select(db.note_version.note_content)
    return dict(rows=rows)

def add_new_note(course_id, user_id):
    #get course_id user_id from request?
    id = db.note_main.insert(course_id = course_id, create_by = user_id)
    db.commit()
    return id

def add_note_version(note_id, user_id,title, content):
    versionId = db.note_version.insert(note_id = note_id, modify_by = user_id, title = title, note_content = content)
    db.commit()
    db(db.note_main.id == note_id ).update(version_id = versionId)
    db.commit()
    return versionId
    
def add_tag(vid, tags):
    nid = db(db.note_version.id == vid).select(db.note_version.note_id)[0].note_id
    db.note_tag.update_or_insert(note_id = nid, version_id = vid, tag = tags)
    db.commit()
    
def delete_tag(version_id, tag):
    db(db.note_tag.version_id == version_id).delete()
    db.commit()


#----------------------------------------------------------#
#interface about message
#----------------------------------------------------------#
def get_messages(user_id):
    query = (db.note_message.user_id == user_id) & (db.note_message.version_id == db.note_version.id)
    #rows = db(query).select(db.note_version.note_id, db.note_version.title, db.note_version.modify_by, db.note_version.modify_on, db.note_message.has_read)
    rows = db(query).select(db.note_version.note_id, db.note_version.id,db.note_version.title, db.note_version.modify_by, db.note_version.modify_on, db.note_message.has_read, db.note_message.id)
    return dict(rows=rows)

def mark_message_read(message_id):
    db(db.note_message.id == message_id).update(has_read = True)
    db.commit()


def add_messages(user_id, version_id):
    db.note_message.insert(user_id = user_id, version_id = version_id, has_read = False)
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
        if row.user_id == user_id and row.relation is not 0:
            notes_list.append(row.note_id)
    return dict(rows=notes_list)


def subscribe_note(note_id, user_id):
    db.note_user_note_relation.update_or_insert((db.note_user_note_relation.note_id==note_id) & (db.note_user_note_relation.user_id==user_id), note_id=note_id, user_id=user_id, relation=1)
    db.commit()


def unsubscribe_note(note_id, user_id):
    db.note_user_note_relation.update_or_insert((db.note_user_note_relation.note_id==note_id) & (db.note_user_note_relation.user_id==user_id), note_id=note_id, user_id=user_id, relation=0)
    db.commit()


def participate_note(note_id, user_id):
    db.note_user_note_relation.update_or_insert((db.note_user_note_relation.note_id==note_id) & (db.note_user_note_relation.user_id==user_id), note_id=note_id, user_id=user_id, relation=2)
    db.commit()
