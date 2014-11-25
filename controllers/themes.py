

def index():
    #session.flash = "Select a theme for your LMS"    
    rows = db(db.theme.name).select()
    images=db(db.image.name).select()
    return dict(rows = rows, images=images)


def theme_picked():
    """
    Build the url to the css style page from arg, 
    and assign it to session.current_theme
    """
    static_subfolder = request.args(0)
    css_filename = request.args(1)

    session.prev_theme = session.current_theme
    
    css_pathname = static_subfolder + '/'  + css_filename
    session.css_pathname = css_pathname
    session.current_theme = URL('static', css_pathname)
    print session.current_theme

	# Get the rows for this css, can just reuse URL as identifier
    picked = db(db.theme.URL == css_pathname).select()
    
    # Get the first use_count for the first row (there should only be one...)
    uses = int(picked[0].use_count) + 1

	# This update syntax works
    db(db.theme.URL == css_pathname).update(use_count=uses)

    #redirect(URL('themes', 'index'))    
    redirect(URL('themes', 'countdown'))

    return dict()

def countdown():
    return dict()

'''
If user rejects theme, they get sent here
'''
def themeBack():

    # delete 1 from theme count for the reject theme
    rejected_theme = db(db.theme.URL == session.css_pathname).select()
    uses = int(rejected_theme[0].use_count) - 1
    db(db.theme.URL == session.css_pathname).update(use_count=uses)

    #reset theme back to previous
    session.current_theme = session.prev_theme
    session.prev_theme = ''
    redirect(URL('themes', 'index'))
    return dict()

def display_popular():
    for row in db(db.theme).select(db.theme.name, orderby=db.theme.use_count*-1, limitby=(0, 3)):
        row.name, row.use_count


def preview():    
   
    if request.args(0) and request.args(1):
        subfolder = request.args(0)
        filename = request.args(1)
        session.preview_theme = subfolder + '/' + filename
       
    else:
        session.preview_theme = 'images/default.jpg'

    return dict()

'''
user can set a course's theme here 

TODO: modify smartgrid to only show certain fields, 
join to themes table to show theme names
'''
@auth.requires(auth.user and auth.user.is_administrator)
def course_themes():
    grid=SQLFORM.smartgrid(db.course, linked_tables=['theme'])

    return dict(grid=grid)
    
def theme_create():

    fp = os.path.join(request.folder,'private','bootstrap.default.json')   

    json_data=open(fp)
    #theme default data
    tdd = json.load(json_data)
    json_data.close()
    calll = '';
    errors = []
    error = '';
    name = ''; filename = ''
    
    if request.post_vars:
        #create theme
        try:
            if request.post_vars['name'] == '':
                errors.append('You need set name')
                raise Exception()
            if request.post_vars['url'] == '':
                errors.append('You need set filename')
                raise Exception()

            name = request.post_vars['name']
            filename = request.post_vars['url']
            fp_less = os.path.join(request.folder,'private','less')  
            fp_copy = os.path.join(request.folder,'private',response.session_id + '_les_' + str(time.time())) 
            fp_css = os.path.join(request.folder,'static','css') 
            shutil.copytree(fp_less, fp_copy)
            var_data = []
            tdd.update(request.post_vars)
            
            for key,value in tdd.iteritems():
                if re.match('/^@/', key):
                  var_data.append(key+': ' + value + ';')
               
            f = open(fp_copy + '/variables.less', 'w')
            f.write("\n".join(var_data))
            f.write('This is a test\n')
            f.close()

            
            calll =  'lesscpy ' + fp_copy + '/bootstrap.less' 
            calll += fp_css + '/' + filename + '.css' 
            os.system(calll)
            #calll(['lesscpy ' + fp_copy + '/bootstrap.less  > ' + fp_css + '/' + response.session_id + '_bootstrap.css'])
            shutil.rmtree(fp_copy)

            db.theme.insert(name=name, 
                URL = 'css/' + filename + '.css',  image_URL = 'images/default.jpg')
            

        except Exception, e:
            error = e
            errors.append('some happend ')

        if len(errors) == 0 :
            redirect(URL('themes', 'index'))   


    return dict(tdd = tdd, calll = calll, errors = errors, error= error, name= name, filename = filename)

