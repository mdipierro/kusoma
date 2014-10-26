'''
####################################################################################################
# dbcal.py
#
#    This file defines the tables used for storing event information,
#    and functions for CRUD operations relating to event information.
#
#    Questions:
#        Should we include the ability to show relevant holidays?
#        Do we need/want a table for "event type" for filtering? Eg: assignment, seminar, etc.
#
####################################################################################################

# Define some useful constants.
NE = IS_NOT_EMPTY()

#########################
# Table definitions
#########################

################################################################################
# event_visibility
#    Defines who can see which events. This allows filtering
#    of events in the calendar.
#
################################################################################
db.define_table(
    'event_visibility',
    Field('event_level', unique=True, requires=NE),
    format='%(event_level)s')
db.event_visibility.id.readable = db.event_visibility.id.writable = False

################################################################################
# cal_event
#    requirements
#      An event must have a start date.
#      An event has an optional end date.
#        Convention: if an event has a start date,
#        but not an end date, then the event is a task.
#
################################################################################
db.define_table(
    'cal_event',
    Field('owner_id', 'reference auth_user'),
    Field('name', requires=NE),
    Field('details', 'text'),
    Field('start_date', 'datetime', requires=NE),
    Field('end_date', 'datetime'),
    Field('visibility', 'reference event_visibilty'),
    auth.signature,
    format='%(name)s')
db.cal_event.id.readable = db.cal_event.id.writable = False

################################################################################
# course_event
#    This table maps courses to events.
#
################################################################################
db.define_table(
    'course_event',
    Field('course_id', 'reference course'),
    Field('event_id', 'reference cal_event'))
db.course_event.id.readable = db.course_event.id.writable = False

#########################
# Function definitions
#########################

################################################################################
# my_events(filter=[])
#    Events for the logged-in user. filter is a list of event_visibility ids
#    of event types to include. Default is an empty list, which means
#    include everything.
#
################################################################################

#########################
# Load defaults
#########################

################################################################################
# Default visiibility levels for events:
#    public: Anyone visiting the site can see, regardless of
#            whether they are logged in.
#    school: Any user logged into the system can see "school" events.
#    class : Only students entrolled in the class and the teacher of the class
#            can see these events when they are logged into the system.
#    staff : Only teachers and adminstrators can see these events
#            when they are logged into the system.
#    admin : Only members of the administrator group can see these events.
#
################################################################################
if db(db.event_visibility).isempty():
    db.event_visibility.bulk_insert([{'event_level':'admin'},
                                     {'event_level':'public'},
                                     {'event_level':'school'},
                                     {'event_level':'class'},
                                     {'event_level':'staff'}])
'''
