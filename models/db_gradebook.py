db.define_table(
    'assignment_grade',
    Field('section_id', 'reference course_section'),
    Field('assignment_id', 'reference homework'),
    Field('user_id', 'reference auth_user'),
    Field('grade', 'float'),
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
    return db(query).select(orderby=db.auth_user.last_name|db.auth_user.first_name)

def get_grades_student(section_id, student_id):
    query = (db.homework.course_section==section_id)
    leftJoin = db.assignment_grade.on((db.homework.id==db.assignment_grade.assignment_id) & (db.assignment_grade.user_id==student_id))

    return db(query).select(left=leftJoin, orderby=db.homework.assignment_order)

def get_final_grade(section_id, student_id):
    query = ((db.course_grade.auth_user == student_id) & (db.course_grade.section_id == section_id))
    return db(query).select()


def get_homework_section(section_id):
    query = (db.homework.course_section==section_id)
    return db(query).select()



def is_user_teacher(section_id):
    return db.membership(course_section=section_id,
                         role='teacher',
                         auth_user=auth.user.id)