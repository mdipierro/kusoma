NE = IS_NOT_EMPTY()

"""
Poll that belongs to a course and user.
"""
db.define_table( 'poll',
                Field( 'title', 'string', requires = NE ),
                Field( 'description', 'string', label = 'Question' ),
                Field( 'auth_user', 'reference auth_user' ),
                Field( 'course_section','reference course_section' ) )
                
"""
Choice that belongs to a poll object.
"""
db.define_table( 'poll_choice',
                Field( 'poll_id', 'reference poll' ),
                Field( 'description', 'string', label = 'choice' ),
                Field( 'allowText', 'boolean', default = False ) )
                
                
"""
Answer that belongs to a choice, which has the user information
"""
db.define_table( 'poll_answer',
                Field( 'choice_id', 'reference poll_choice' ),
                Field( 'auth_user', 'reference auth_user' ),
                #Field( 'answer', 'boolean', default = False ), #probably unneeded; only 'true' choices will be registered
                Field( 'answerText', 'string' ) )
                
"""
Useful queries for polling
"""
# All items for a single queried poll
ALL_RESPONSES_FOR_POLL = ( db.poll_choice.poll_id == db.poll.id )
# all responses that have been chosen by users on a poll
ALL_ANSWERED_FOR_POLL = ( db.poll_answer.choice_id == ALL_RESPONSES_FOR_POLL )
#...does the above work?