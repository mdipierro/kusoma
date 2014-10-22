/*global window, document, $, moment */
/**
LMS299 Calendar Control
**/
(function ($, window, undefined, moment) {
   /**
    The fullcalendar.js is wrapped inside of a jQueryUI Widget.  This will provide us
    with the ability to create a reusable JS calendar control that has a standardized style
    and is already connected to the LMS299 event data source.  If a fullcalendar feature needs
    to be exposed, it can be exposed through the options object.  
    
    If extra features are added beyond what fullcalendar can do (such as filtering LSM299 events 
    or additional UI tools) they can also be exposed through the options object, and will be 
    available wherever this widget is used on the site.  See the width option for this calendar
    control for an example of an expanded feature.

    Documentation on the jQueryUI factory can be found at http://api.jqueryui.com/jQuery.widget/

    Questions about this file can be sent to mikesherry24@gmail.com

    example usage
    $(document).ready(function() {
        $('#fullcalendar').fullCalendar({
            disabled: false,
            headerCenter: 'month,basicWeek',
            height: 500p,
            view: 'month',
            width: 500           
        });
    });
   **/
    $.widget('lms299.lmsCalendar', {
        options: {
            created: false,
            disabled: false,
            events: {},
            headerCenter: 'month,basicWeek',
            headerLeft: 'title',
            headerRight: 'today prev,next',
            height: 'auto',
            view: 'month',
            width: ''
        },
        _create: function (options) {
            var self = this;
        },
        _init: function () {
            var self = this;
            if (!self.options.created) {
                    self._createCalendar();
                }
                self.options.created = true;
            },
        _createCalendar: function () {
            var self = this;
            self.element.addClass('lms299-calendar');
            self._container = $('<div id="lms299calendar-container"></div>').appendTo(this.element);
            $('#lms299calendar-container').fullCalendar({
                header: {        
                    left:   self.options.headerLeft,
                    center: self.options.headerCenter,
                    right:  self.options.headerRight
                },       
                events: self.options.events,
                height: self.options.height
            });
            if (self.options.width !== '') {
                $('#lms299calendar-container').width(self.options.width);
            }
        }
    });
}(jQuery, window, document, moment));



