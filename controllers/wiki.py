# This is the wiki controller for the lms299.
def wiki():
     """ this controller returns a dictionary rendered by the view
         it lists all wiki pages
     >>> index().has_key('pages')
     True
     """
    #  return dict()
     pages = db().select(db.wikipage.id,db.wikipage.title,orderby=db.wikipage.title)
     return dict(pages=pages)

@auth.requires_login()
def wikicreate():
     """creates a new empty wiki page"""
<<<<<<< HEAD
     form = SQLFORM(db.wikipage).process(next=URL('index'))
=======
     form = SQLFORM(db.wikipage).process(next=URL('wiki'))
>>>>>>> 74ed9a7704d97630a4d91272c68760558305ce49
     return dict(form=form)

def wikishow():
     """shows a wiki page"""
<<<<<<< HEAD
     this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
     db.post.page_id.default = this_page.id
     form = SQLFORM(db.post).process() if auth.user else None
     pagecomments = db(db.post.page_id==this_page.id).select()
=======
     this_page = db.wikipage(request.args(0,cast=int)) or redirect(URL('wiki'))
     db.wikipost.page_id.default = this_page.id
     form = SQLFORM(db.wikipost).process() if auth.user else None
     pagecomments = db(db.wikipost.page_id==this_page.id).select()
>>>>>>> 74ed9a7704d97630a4d91272c68760558305ce49
     return dict(page=this_page, comments=pagecomments, form=form)


def wikisearch():
     """an ajax wiki search page"""
     return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
              _onkeyup="ajax('callback', ['keyword'], 'target');")),
              target_div=DIV(_id='target'))
<<<<<<< HEAD
=======

@auth.requires_login()
def wikiedit():
     """edit an existing wiki page"""
     this_page = db.wikipage(request.args(0,cast=int)) or redirect(URL('wiki'))
     form = SQLFORM(db.wikipage, this_page).process(
         next = URL('show',args=request.args))
     return dict(form=form)
>>>>>>> 74ed9a7704d97630a4d91272c68760558305ce49
