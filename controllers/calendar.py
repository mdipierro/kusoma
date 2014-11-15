# -*- coding: utf-8 -*-
# This is the controller file for the lms299 event calendar.
import datetime

@auth.requires_login()
def index():
    # start = first_of_month().strftime('%Y-%m-%d')
    # end = last_of_month().strftime('%Y-%m-%d')
    # params = {'start': start, 'end': end}
    return dict(selectedCourseEvents=my_events(datetime.date.min, datetime.date.max))
    #return dict()

@auth.requires_login()
def calendar():
    return dict()

#@auth.requires_login()
@auth.requires(auth.user.is_teacher==True or auth.user.is_administrator==True) 
def create():
    # Display a form the user can use to create a new event.
    #
    # The form should allow the user to select a course.
    #
    # When the event is created in db.cal_event, a record is also created in db.course_event
    # where the course_id is the course that the user selected and the referenced event is the
    # record just created in db.cal_event
    form = SQLFORM(db.cal_event).process()
    if form.accepted:
        response.flash = 'Event created successfully'
    elif form.errors:
        response.flash = 'Form has some error, REVIEW please !'
    else :
        response.flash = 'Please fill in the form !'
    return dict(form=form)

#@auth.requires_login()
@auth.requires(auth.user.is_teacher==True or auth.user.is_administrator==True)
def manage():
    # get a list of events that the current user created
    # display the events in a grid or a picklist
    # The user can selects an event and clicks a delete button
    # Delete the event that the user selected
    return dict(grid=SQLFORM.smartgrid(db.cal_event))
    
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
    # The view will use the object as a datasource for fullcalendar and display the events
    selectedCourse = request.vars.selectedCourse
    rows = ''
    selectedCourseEvents = ''
    if selectedCourse:
        query = db.course_section.name == selectedCourse
        rows = db(query).select()
        if len(rows) == 0:
            response.flash = 'Course section is not valid'
        elif not is_user_student(rows[0].id) and not is_user_teacher(rows[0].id):
            response.flash = 'You are not authorized to view the events for this course section'
        else:
            selectedCourseEvents = course_events(datetime.date.min, datetime.date.max, rows[0].course.id)
    return dict(myCourses = my_sections(), rows = rows, selectedCourseEvents = selectedCourseEvents, selectedCourse = selectedCourse)
