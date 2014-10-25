# -*- coding: utf-8 -*-
# This is the controller file for the lms299 event calendar.

def calendar():
    return dict()

def create_event():
    # Display a form the user can use to create a new event.
    #
    # The form should allow the user to select a course.
    #
    # When the event is created in db.cal_event, a record is also created in db.course_event
    # where the course_id is the course that the user selected and the referenced event is the
    # record just created in db.cal_event
    form = SQLFORM(db.cal_event).process(next=URL('calendar'))
    return dict(form=form)

def delete_event():
    # get a list of events that the current user created
    # display the events in a grid or a picklist
    # The user can selects an event and clicks a delete button
    # Delete the event that the user selected
    return dict()
    
def user_calendar():
    # input: a user id
    #
    # Run a query to select all of the events that the user is allowed to see
    #
    # Convert the queried events into a json object and return the json object to be used in the view
    #
    # The view will use the json object as a datasource for fullcalendar and display the events
    return dict()

def course_calendar():
    # input: a course ID
    #
    # With the given course ID, query all of the events related to that course
    #
    # Convert the queried events into a json object and return the json object to be used in the view
    #
    # The view will use the json object as a datasource for fullcalendar and display the events
    return dict()
