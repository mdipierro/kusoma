#Constants
NE = IS_NOT_EMPTY()

from gluon.tools import *
auth = Auth(db)

'''
Stores lecture and supplementary video recordings
'''

db.define_table('recording',
    Field('youtube_id', requires=NE),
    Field('course_id', 'reference course_section',
          required=IS_IN_DB(db, db.course_section.id, '%(name)s')),
    Field('recorder', 'reference auth_user', default=auth.user_id),
    Field('class_date', 'datetime', default=request.now, requires=NE),
    Field('is_class', 'boolean', default=True, requires=NE)
    )

#Some sample videos for testing
db.recording.truncate()
db.recording.insert(youtube_id='M5IPlMe83yI',course_id=1,recorder=1)
db.recording.insert(youtube_id='iMUX9NdN8YE',course_id=1,recorder=1)
db.recording.insert(youtube_id='-eztsQogulk',course_id=1,recorder=1)
db.recording.insert(youtube_id='VTJFvi0L-MI',course_id=1,recorder=1)
