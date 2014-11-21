"use strict";
(function($, application, window) {

    Handlebars.registerHelper('json', function (context) {
        return JSON.stringify(context);
    });


    application.CommunicationLayer = function (spec) {
        var self = this;
        //hardcode author as "Current User"
        //normally, you might pull this from a cookie or something
        self.author = "Current User";
        
        self.insert = function (comment, callback) {
            //send data to server via AJAX
            //server returns the inserted comment ID
            //trigger callback method with comment data
            
            //emulate inserted comment by triggering callback
            //with a dummy ID
            callback({
                id: comment.parentId + 1000,
                body: comment.body,
                date: new Date(),
                author: self.author
            });
        };

        self.delete = function(id) {
            //delete comment
        };

        self.update = function(toUpdate, callback) {
            //update comment
            
            callback();
        };

        return self;
    };


    application.bindCommentApp = function(app, selector) {
        var $wrapper = $(selector || window.document);

        $wrapper
            //PRIMARY BINDINGS
            .on('click', '.-delete', function() {
                var $comment = $(this).closest(".-comment"),
                    data = $comment.data("app");
                var proceed = confirm("Are you sure you would like to delete this comment?");
                if (!proceed) { return; }
                app.delete(data.id);
                $comment.remove();
            })
            .on('click', '.-reply', function () {
                var $comment = $(this).closest(".-comment"),
                    data = $comment.data("app");

                var $children = $comment.find(".-child-comments").first();
                $('#add-comment-template').load('../static/js/note_addcomment.hbs', 
                                                function(){
                                                        var addCommentTemplate = Handlebars.compile($("#add-comment-template").html());
                                                        //insert the add comment form template into children list
                                                        $children.prepend(addCommentTemplate({parentId: data.id}));
                                                    });
                
            })
            .on('click', '.-update', function () {
                var $comment = $(this).closest(".-comment"),
                    data = $comment.data("app");

                var $body = $comment.find(".-body").first();
                var body = $body.text();
                $body.empty();
            
                $('#comment-update-template').load('../static/js/note_updatecomment.hbs',
                                                   function (){
                                                                    var commentUpdateTemplate = Handlebars.compile($("#comment-update-template").html());            
                                                                    $body.html(commentUpdateTemplate({ body: body }));

                                                            });
            

            })


            //TEMPLATE RELATED BINDINGS
            .on('submit', '.-add-comment-form', function () {
                var $this = $(this),
                    $tmpl = $this.closest(".-add-comment-template"),
                    $children = $this.closest(".-child-comments"),
                    data = $this.data("app"),
                    body = $this.find(".-body").val();

                $tmpl.remove();
            
                $('#comment-template').load('../static/js/note_showcomment.hbs',
                                            function (){
                                                        var commentTemplate = Handlebars.compile($("#comment-template").html());
                                                        app.insert({ parentId: data.parentId, body: body }, function (comment) {
                                                            $children.prepend(commentTemplate(comment));
                                                        });
                                                });

                return false; //prevent post
            })
            .on('click', '.-add-comment-form .-cancel', function () {
                var $tmpl = $(this).closest(".-add-comment-template");

                $tmpl.remove();
            })
        
            .on('submit', '.-update-comment-form', function () {
                var $tmpl = $(this).closest(".-update-comment-form"),
                    $comment = $tmpl.closest(".-comment"),
                    $body = $comment.find(".-body").first(),
                    data = $comment.data("app"),
                    body = $tmpl.find(".-value").val();

                $body.empty();
                app.update({ id: data.id, body: body }, function () {
                    $body.text(body);
                });

                return false; //prevent post
            })
            .on('click', '.-update-comment-form .-cancel', function () {
                var $tmpl = $(this).closest(".-update-comment-form"),
                    $body = $tmpl.closest(".-comment").find(".-body").first(),
                    originalValue = $tmpl.find(".-original").val();
                $body.text(originalValue);
                $tmpl.remove();
                
            })


        ;
    };




})(jQuery, window.MyApp || (window.MyApp = {}), window);

$(function() {
    MyApp.bindCommentApp(new MyApp.CommunicationLayer(), "#comment-wrapper");
});