
@auth.requires_login
def index():
    section_id = request.args(0,cast=int)
    return dict()