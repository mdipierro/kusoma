/*global window, document, $, moment */
/**
LMS299 Calendar Control
**/
(function ($, window, undefined, moment) {
   /**
    example usage
    $(document).ready(function() {
        $('#fullcalendar').fullCalendar({
            disabled: false,
            created: false
        });
    });
   **/
    $.widget('lms299.lmsCalendar', {
        options: {
            created: false,
            disabled: false,
            headerCenter: 'month,basicWeek,basicDay',
            headerLeft: 'title',
            headerRight: 'today prev,next',
            height: 'auto',
            view: 'month'
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
            //self.element.click(this.options.click);
            //self._setDisabled(self.options.disabled);
            //self.element.css('height', self.options.height);
            //self.element.css('line-height', self.options.height - 5 + 'px');
            //self.element.addClass('dr-crm-button-hover');
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
        }
    });
}(jQuery, window, document, moment));



