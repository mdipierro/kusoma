# -*- coding: utf-8 -*-
# This is the controller file for the lms299 event calendar.
import datetime

@auth.requires_login()
def index():
    # start = first_of_month().strftime('%Y-%m-%d')
    # end = last_of_month().strftime('%Y-%m-%d')
    # params = {'start': start, 'end': end}
    # return dict(form=my_events(start, end), params=params)
    return dict()

@auth.requires_login()
def calendar():
    return dict()

@auth.requires_login()
def create_event():
    # Display a form the user can use to create a new event.
    #
    # The form should allow the user to select a course.
    #
    # When the event is created in db.cal_event, a record is also created in db.course_event
    # where the course_id is the course that the user selected and the referenced event is the
    # record just created in db.cal_event
    form = SQLFORM(db.cal_event).process(next=URL('calendar'))
    if form.accepts(request, session, dbio=False):
        add_event(title=form.vars.title,
                  details=form.vars.details,
                  start_date=form.vars.start_date,
                  end_date=form.vars.end_date,
                  all_day=form.vars.all_day,
                  url=form.vars.url,
                  visibility=form.vars.visiblity,
                  course_id=form.vars.course_id)
                  
    return dict(form=form)

@auth.requires_login()
def delete_event():
    # get a list of events that the current user created
    # display the events in a grid or a picklist
    # The user can selects an event and clicks a delete button
    # Delete the event that the user selected
    return dict()
    
@auth.requires_login()
def user_calendar():
    # input: a user id
    #
    # Run a query to select all of the events that the user is allowed to see
    #
    # Convert the queried events into a json object and return the json object to be used in the view
    #
    # The view will use the json object as a datasource for fullcalendar and display the events
    return dict()

@auth.requires_login()
def course_calendar():
    # input: a course ID passed in through the session object
    # use course picker list to select a course
    # With the given course ID, query all of the events related to that course
    #
    session.selectedCourse = 'CSC205-701'
    if session.selectedCourse:
        query = db.course_section.name == session.selectedCourse
        rows = db(query).select()
        selectedCourseEvents = course_events(datetime.date.min, datetime.date.max, rows[0].course.id)
    # The view will use the object as a datasource for fullcalendar and display the events
    return dict(session = session, selectedCourseEvents = selectedCourseEvents, myCourses = my_sections(), rows = rows)
