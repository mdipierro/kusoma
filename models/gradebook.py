db.define_table(
    'assignment_grade',
    Field('section_id', 'reference course_section'),
    Field('assignment_id', 'reference homework'),
    Field('user_id', 'reference auth_user'),
    Field('grade', 'integer'),
    Field('assignment_comment')
)

db.define_table(
    'course_grade',
    Field('section_id', 'reference course_section'),
    Field('auth_user', 'reference auth_user'),
    Field('grade'),
    Field('teacher_comment'))

def get_all_students(section_id):
    query = (db.membership.course_section==section_id)&(db.membership.auth_user==db.auth_user.id)&(db.membership.role!='teacher')
    return db(query).select()

 


def is_user_teacher(section_id):
    return db.membership(course_section=section_id,
                         role='teacher',
                         auth_user=auth.user.id)