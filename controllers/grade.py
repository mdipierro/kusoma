# -*- coding: utf-8 -*-
# try something like
def index():
    return dict(message="hello just testing!!")

def teacher():
    response.files.insert(0,URL('static','js/jquery.js'))
    response.files.insert(0,URL('static','js/jquery.handsontable.full.js'))
    response.files.insert(0,URL('static','css/jquery.handsontable.full.css'))

    session.flash = 'Welcome Teacher'
    return dict(role="Teacher")

def student():
    session.flash = 'Welcome Student'
    return dict(role="student")