# -*- coding: utf-8 -*-
    
@auth.requires_login()
def polls():
    """
    List of all polls for the course section
    """
    
    section_id = request.args(0,cast=int)
    
    query = db.poll.course_section==section_id
    
    polls = db(query).select()
    return dict(polls = polls)