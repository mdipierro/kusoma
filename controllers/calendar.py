# -*- coding: utf-8 -*-
# This is the controller file for the lms299 event calendar.
#
# Ideas for future enhancements:
#   Have FullCalendar send the view state as a json object,
#   (as a var value?) which is then stored in a session variable.
#   That way we can restore the proper view state when we return
#   the user to the calendar.
#
import datetime

#@auth.requires_login()

@auth.requires(CAN_MANAGE_EVENTS)
def create():
    """
    Display a form the user can use to create a new event.
    
    The form should allow the user to select a course.
    
    When the event is created in db.cal_event, a record is also created in db.course_event
    where the course_id is the course that the user selected and the referenced event is the
    record just created in db.cal_event
    """
    end = None
    if request.args:
        start = _convert_string_to_date(request.args(0), fmt=OUTPUT_DATE_FORMAT)
        if request.args(1):
            end = _convert_string_to_date(request.args(1), fmt=OUTPUT_DATE_FORMAT)
    else:
        start = datetime.datetime.today()
        # We re-create the date so the time is 00:00:00, rather than the current time.
    	start = datetime.datetime(start.year, start.month, start.day)
    db.cal_event.start_date.default = start
    db.cal_event.end_date.default = end
    url = URL('calendar', 'my_calendar')
    form = SQLFORM(db.cal_event).process()
    if form.accepted:
        session.flash = 'Event created successfully'
        redirect(url)
    elif form.errors:
        response.flash = 'There are errors on the form, please review.'
    return dict(form=form)

#@auth.requires_login()
@auth.requires(CAN_MANAGE_EVENTS)
def manage():
    """
    Get a list of events that the current user created
    display the events in a grid or a picklist.
    The user can selects an event and clicks a delete button.
    Delete the event that the user selected.
    """
    return dict(grid=SQLFORM.smartgrid(db.cal_event))

@auth.requires_login()
def my_calendar():
    """
    input: a course ID passed in through the session object
    use course picker list to select a course
    With the given course ID, query all of the events related to that course
    The view will use the object as a datasource for fullcalendar and display the events
    """
    rows = ''
    selectedCourse = request.vars.selectedCourse
    if selectedCourse:
        query = db.course_section.name == selectedCourse
        rows = db(query).select()
        if len(rows) == 0:
            response.flash = 'Course section is not valid'
        elif not is_user_student(rows[0].id) and not is_user_teacher(rows[0].id):
            response.flash = 'You are not authorized to view the events for this course section'
        else:
            selectedCourseEvents = course_events(datetime.date.min, datetime.date.max, rows[0].course.id)
    else:
        selectedCourseEvents = my_events(datetime.date.min, datetime.date.max, True)
    return dict(myCourses = my_sections(), rows = rows, selectedCourseEvents = selectedCourseEvents, selectedCourse = selectedCourse)
