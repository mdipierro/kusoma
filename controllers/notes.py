# -*- coding: utf-8 -*-
# try something like
import time

def index():
    return dict(message="hello just testing!!")

def get_all_notes():
    return db().select(db.note_main.All)

def add_note(course_id, tag):
    db.notes_main.insert(course_id = course_id, tag = tag, create_on = time.time())
    db.commit()
