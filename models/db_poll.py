#Poll (ID, Name, title, description/question, userID, courseID)
#Choice (PollID, description, true/false…?)

#Something to register the user and the options chosen…?

#Answer table that links the question ID with the student/user and the
#chosen answer

#Give them an option to add some sort of answer.



NE = IS_NOT_EMPTY()

"""
Poll that belongs to a course and user.
"""
db.define_table( 'poll',
                Field( 'title', 'string', requires = NE ),
                Field( 'description,', 'string', label = 'Question' ),
                Field( 'auth_user', 'reference auth_user' ),
                Field( 'course_section','reference course_section' ) )
                
"""
Choice that belongs to a poll object.
"""
db.define_table( 'choice',
                Field( 'poll', 'reference poll' ),
                Field( 'description', 'string', label = 'choice' ),
                Field( 'allowText', 'boolean', default = False ) )
                
                
"""
Answer that belongs to a choice, which has the user information
"""
db.define_table( 'answer',
                Field( 'choice', 'reference choice' ),
                Field( 'auth_user', 'reference auth_user' ),
                Field( 'answer', 'boolean', default = False ),
                Field( 'answerText', 'string' ) )
                
                #Let's not worry about string answers... actually
                #I've added possible text entry support
                
                #db1 has some ideas on validation - checking whether
                #a student is in the class or not... et cetera.
                #Though... how could a student GET to the poll if they aren't
                #enrolled in that class to begin with?  What?
                #Also, such methods are apparently already written in
                #db1.py.  I'm sure you can use those.
                
                #add poll to the menu items if you are a teacher...?
                #this is when you're in the section specific page
                
                #You can give names to queries:
#PERSONAL_EVENTS = (db.cal_event.owner_id == auth.user_id)
                #You may want to do this to grab questions for a specific
                #poll and such
                
                #newest version of dbcal.py has code that does things
                #if you aren't authorized to create a cal_event.
                #it redirects you...
                #and... line 149 ish, there are things to authorize editing
                #an event... perhaps you should do that, too.
                #calendar.py and dbcal.py can help if you look at the stuff
                #inside...
                
                #Also, I'm sure the NE at the top can be deleted, since it's
                #already defined elsewhere
                #But... test it.
                
                #There should now be an 'exception' thing in db.py.
                #use this for exception stuff.
                
                #Think of how his quiz thing worked.  This is basically the
                #same thing you want to create
                
                #in the menu, there's a 'poll' option, then if you click it
                #and it takes you to a page that gives you a list of polls
                #with the option next to each to edit them, and an option at
                #the top to create a new one.
                #...
                #Actually, put it under the 'course content' or... one of
                #those tabs...
                
                #hmm... right.  Look at the examples on the site if you
                # want more help