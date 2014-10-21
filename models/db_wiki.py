#This is wiki table setting file

from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('wikipage',
    Field('title'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(title)s')

db.define_table('wikipost',
    Field('page_id', 'reference wikipage'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id))

db.define_table('wikidocument',
    Field('page_id', 'reference wikipage'),
    Field('name'),
    Field('files', 'upload'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(name)s')

db.wikipage.title.requires = IS_NOT_IN_DB(db, 'page.title')
db.wikipage.body.requires = IS_NOT_EMPTY()
db.wikipage.created_by.readable = db.wikipage.created_by.writable = False
db.wikipage.created_on.readable = db.wikipage.created_on.writable = False

db.wikipost.body.requires = IS_NOT_EMPTY()
db.wikipost.page_id.readable = db.wikipost.page_id.writable = False
db.wikipost.created_by.readable = db.wikipost.created_by.writable = False
db.wikipost.created_on.readable = db.wikipost.created_on.writable = False

db.wikidocument.name.requires = IS_NOT_IN_DB(db, 'document.name')
db.wikidocument.page_id.readable = db.wikidocument.page_id.writable = False
db.wikidocument.created_by.readable = db.wikidocument.created_by.writable = False
db.wikidocument.created_on.readable = db.wikidocument.created_on.writable = False
