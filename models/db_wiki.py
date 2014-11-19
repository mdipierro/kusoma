#This is wiki table setting file

from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('wikipage',
    Field('title'),
    Field('body', 'text'),
    auth.signature,                
    format='%(title)s')

db.wikipage._enable_record_versioning()

db.define_table('wikipost',
    Field('page_id', 'reference wikipage'),
    Field('body', 'text'),
    auth.signature)                

db.define_table('wikidocument',
    Field('page_id', 'reference wikipage'),
    Field('name'),
    Field('files', 'upload'),
    auth.signature,
    format='%(name)s')

db.wikipage.title.requires = IS_NOT_IN_DB(db, 'wikipage.title')
db.wikipage.body.requires = IS_NOT_EMPTY()
db.wikipost.body.requires = IS_NOT_EMPTY()
db.wikipost.page_id.readable = db.wikipost.page_id.writable = False
db.wikidocument.name.requires = IS_NOT_IN_DB(db, 'wikidocument.name')
db.wikidocument.page_id.readable = db.wikidocument.page_id.writable = False
