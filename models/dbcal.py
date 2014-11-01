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
from datetime import datetime, date, timedelta
DEBUG = True
DATE_FORMAT = '%Y-%m-%d'

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
# db.event_visibility.id.readable = db.event_visibility.id.writable = False

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
    'cal_event',                                                         ## (id) FC Event field
    Field('owner_id', 'reference auth_user', default=auth.user_id),
    Field('title', requires=NE),                                         ## FC Event field
    Field('details', 'text'),
    Field('start_date', 'datetime', requires=NE),                        ## FC Event field
    Field('end_date', 'datetime'),                                       ## FC Event field
    Field('all_day', 'boolean', default=False),                          ## FC Event field
    Field('url'),                                                        ## FC Event field
    Field('visibility', 'reference event_visibility'),
    Field('course_id', 'reference course', required=False, requires=IS_EMPTY_OR(IS_IN_DB(db, 'course.id'))),
    auth.signature,
    format='%(title)s')
db.cal_event.id.readable = db.cal_event.id.writable = False
db.cal_event.owner_id.readable = db.cal_event.owner_id.writable = False

# We use auth.user_id because it doesn't throw an exception when noone is logged in.
DATE_DEFAULTS = ['start', 'end']
PERSONAL_EVENTS = (db.cal_event.owner_id == auth.user_id)
PUBLIC_EVENTS = (db.event_visibility.visibility=='public')
MY_EVENTS = (PERSONAL_EVENTS | PUBLIC_EVENTS)
NO_END_DATE = (db.cal_event.end_date == None)
EVENT_FIELDS = [db.cal_event.id,
                db.cal_event.owner_id,
                db.cal_event.title,
                db.cal_event.details,
                db.cal_event.start_date,
                db.cal_event.end_date,
                db.cal_event.all_day,
                db.cal_event.url,
                db.event_visibility.visibility,
                db.cal_event.visibility,
                db.cal_event.course_id]

def STARTS_AFTER_DATE(date):
    return (db.cal_event.start_date >= date)

def ENDS_BEFORE_DATE(date):
    return (db.cal_event.end_date <= date)

def NO_END_DATE_OR_ENDS_BEFORE_DATE(date):
    return (NO_END_DATE | ENDS_BEFORE_DATE(date))

def IS_IN_DATE_RANGE(start_date, end_date=None):
    return (STARTS_AFTER_DATE(start_date) | NO_END_DATE_OR_ENDS_BEFORE_DATE(end_date))

def COURSE_EVENTS(course_id):
    return (db.cal_event.course_id == course_id)

#########################
# Classes
#########################
# class CalendarEvent(object):
#     def __init__(self, owner_id, title, start, visibility, details='',
#                  end=None, course=None, event_id=None, allDay=False):
#         self.id = event_id
#         self.owner_id = owner_id
#         self.name = title
#         self.details = details
#         self.start_date = start
#         self.end_date = end
#         self.all_day = allDay
#         self.visibility = visibility
#         self.course = course

#########################
# Function definitions
#########################

def add_event(title, visibility, owner=auth.user_id, details='',
              start_date=date.today(), end_date=None, all_date=False, url=None, course_id=None):
    """
    Add a new event to the table.
    """
    from datetime import datetime
    if start_date:
        start = datetime.strptime(start_date, DATE_FORMAT)
    else:
        start = _first_of_month()
    if end_date:
        end = datetime.strptime(end_date, DATE_FORMAT)
    else:
        end = None
    db.cal_event.insert(ower_id=owner,
                        title=title,
                        details=details,
                        start_date=start,
                        end_date=end,
                        all_day=all_day,     ## Fix this to insert False when we get a None
                        url=url,
                        visibility=visibility,
                        course_id=course_id)

def my_events(start_date, end_date, json=False):
    """
    Events for the logged-in user.
    """
    from datetime import datetime
    if start_date:
        start = datetime.strptime(start_date, DATE_FORMAT)
    else:
        _first_of_month()
    if end_date:
        end = datetime.strptime(end_date, DATE_FORMAT)
    else:
        end = _last_of_month()
    try:
        query = (MY_EVENTS &
                 IS_IN_DATE_RANGE(start, end) &
                 (db.cal_event.visibility == db.event_visibility.id))
    except:
        return
    if json:
        return _get_events_json(query, EVENT_FIELDS, db.cal_event.id)
    else:
        return _get_events(query, EVENT_FIELDS, db.cal_event.id)

def course_events(start_date, end_date, course_id):
    """
    Events for the selected-course-in user.
    """
    from datetime import datetime
    if start_date:
        start = datetime.strptime(start_date, DATE_FORMAT)
    else:
        _first_of_month()
    if end_date:
        end = datetime.strptime(end_date, DATE_FORMAT)
    else:
        end = _last_of_month()
    try:
        query = (COURSE_EVENTS &
                 IS_IN_DATE_RANGE(start, end) &
                 (db.cal_event.visibility == db.event_visibility.id))
        # query = ((db.cal_event.course_id == course_id) &
        #          (db.cal_event.visibility == db.event_visibility.id) &
        #          (db.cal_event.start_date >= start_date) &
        #          ((db.cal_event.end_date == None) | (db.cal_event.end_date <= end_date)))
        # fields = [db.cal_event.id,
        #           db.cal_event.owner_id,
        #           db.cal_event.title,
        #           db.cal_event.details,
        #           db.cal_event.start_date,
        #           db.cal_event.end_date,
        #           db.event_visibility.visibility,
        #           db.cal_event.visibility]
    except:
        return
    return _get_events_json(query, fields)

def _get_events(query, fields, groupby=None):
    return  db(query).select(*fields, groupby=groupby)

def _get_events_json(query, fields, groupby=None):
    ############## Refactor this ##############
    # To do:
    # This needs error handling
    # Choose date format based on whether the event is associated with a specific time.
    # I'm not 100% comfortable with the groupby, but it gets rid of duplicates.
    #    We'll need to keep an eye on it.
    events = _get_events(query, fields, groupby)
    cal = []
    for evt in events:
        c = {'id': evt.cal_event.id,
             'owner_id' : evt.cal_event.owner_id,
             'title': evt.cal_event.title,
             'details': evt.cal_event.details,
             'start': evt.cal_event.start_date.strftime('%Y-%m-%d'),
             'allDay': evt.cal_event.all_day,
             'url': evt.cal_event.url,
             'visibility': evt.event_visibility.visibility,
             'vis_code': evt.cal_event.visibility,
             'course_id': evt.cal_event.course_id}
        if evt.cal_event.end_date:
            c['end'] = evt.cal_event.end_date.strftime('%Y-%m-%d')
        cal.append(c)
    return cal

def _first_of_month():
    first = datetime.date.today()
    first = first.replace(day=1)
    return first

def _last_of_month():
    last = datetime.date.today()
    last = datetime.date(last.year, last.month + 1, 1)
    last = last + timedelta(days=-1)
    return last

def _convert_string_to_date(date, default=None):
    from datetime import datetime
    if date:
        return datetime.strptime(date, DATE_FORMAT)
    else:
        if default:
            if default == DATE_DEFAULTS['start']:
                return _first_of_month()
            elif default == DATE_DEFAULTS['end']:
                return _last_of_month()
            else:
                return None
        else:
            return None

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
#         # auth.get_`or_create_user(first_name='Bryan',
#         #                         last_name='Patzke',
#         #                         email='bryan.patzke@insignis.com',
#         #                         password=CRYPT('bobbob'))
#         populate(db.auth_user, 5)
#     if db(db.cal_event).isempty():
#         populate(db.cal_event, 10)
