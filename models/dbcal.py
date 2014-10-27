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
from datetime import date
DEBUG = True

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
    Field('visibility', unique=True, requires=NE),
    format='%(visibility)s')
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
    'cal_event',                                        ## (id) FC Event field
    Field('owner_id', 'reference auth_user', default=auth.user_id),
    Field('title', requires=NE),                        ## FC Event field
    Field('details', 'text'),
    Field('start_date', 'datetime', requires=NE),       ## FC Event field
    Field('end_date', 'datetime'),                      ## FC Event field
    Field('allDay', 'boolean', default=False),          ## FC Event field
    Field('url'),                                       ## FC Event field
    Field('visibility', 'reference event_visibility'),
    auth.signature,
    format='%(title)s')
db.cal_event.id.readable = db.cal_event.id.writable = False
db.cal_event.owner_id.readable = db.cal_event.owner_id.writable = False

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
# Classes
#########################

class CalendarEvent(object):
    def __init__(self, owner_id, title, start, visibility, details='',
                 end=None, course=None, event_id=None, allDay=False):
        self.id = event_id
        self.owner_id = owner_id
        self.name = title
        self.details = details
        self.start_date = start
        self.end_date = end
        self.all_day = allDay
        self.visibility = visibility
        self.course = course
    # def __call__(self):
    #     return dict(populate dict with object fields)

#########################
# Function definitions
#########################

# def add_event(event_name, event_visibility, owner=auth.user_id, event_details='',
#               event_start_date=date.today(), event_end_date=None, event_course_id=None):
def add_event(event):
    """
    Add a new event to the table.
    """
    if db(db.cal_event.id == event.id).count() == 0:
        new_id = db.cal_event.insert(ower_id=event.owner_id,
                                     name=event.name,
                                     details=event.details,
                                     start_date=event.start_date,
                                     end_date=event.end_date,
                                     visibility=event.visibility)
        event.id = new_id
        if event.course:
            db.course_event.insert(couse_id=course_id, event_id=new_id)
    return event

def my_events():
    """
    Events for the logged-in user.
    """
    events =  db((db.cal_event.owner_id == auth.user.id) &
                 (db.cal_event.owner_id == db.auth_user.id) &
                 (db.cal_event.visibility == db.event_visibility.id)).select(db.cal_event.id,
                                                                             db.cal_event.owner_id,
                                                                             db.cal_event.name,
                                                                             db.cal_event.details,
                                                                             db.cal_event.start_date,
                                                                             db.cal_event.end_date,
                                                                             db.event_visibility.visibility,
                                                                             orderby=~db.cal_event.start_date)
    cal = []
    for e in events:
        cal.append(CalendarEvent(event_id=e.id,
                                 owner_id=e.owner_id,
                                 title=e.name,
                                 details=e.details,
                                 start=e.start_date,
                                 visibility=e.visibility,
                                 end=e.end_date))
    return cal
                                 

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
    db.event_visibility.bulk_insert([{'visibility':'admin'},
                                     {'visibility':'public'},
                                     {'visibility':'school'},
                                     {'visibility':'class'},
                                     {'visibility':'staff'}])
# if DEBUG:
#     from gluon.contrib.populate import populate
#     if db(db.auth_user).count() == 1:
#         # auth.get_or_create_user(first_name='Bryan',
#         #                         last_name='Patzke',
#         #                         email='bryan.patzke@insignis.com',
#         #                         password=CRYPT('bobbob'))
#         populate(db.auth_user, 5)
#     if db(db.cal_event).isempty():
#         populate(db.cal_event, 10)
