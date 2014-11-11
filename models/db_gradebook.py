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
    Field('teacher_comment', 'text'))

db.define_table(
    'section_statistics',
    Field('section_id', 'reference course_section'),
    Field('min_score', 'boolean'),
    Field('max_score','boolean'),
    Field('avg_score','boolean'),
    Field('median_score','boolean'),
    Field('mean_score','boolean'),
    Field('sum_score','boolean'),
    Field('cov','boolean'),
    Field('var','boolean'),
    Field('std','boolean'),
)

def get_statistics(section_id):
    query = (db.section_statistics.section_id==section_id)
    return db(query).select()

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


def get_homework_stats(section_id):
    query = (db.assignment_grade.section_id==section_id)
    sel = db.assignment_grade.grade.max() | db.assignment_grade.grade.min() | db.assignment_grade.grade.avg()
    groupby = db.assignment_grade.assignment_id | db.homework.name
    leftJoin = db.assignment_grade.on(db.homework.id==db.assignment_grade.assignment_id)

    return db(query).select(sel,groupby, left=leftJoin, groupby = groupby, orderby=db.homework.assignment_order)

def get_assignment_by_homework(section_id, homework_id):
    query = (db.assignment_grade.section_id==section_id) & (db.assignment_grade.assignment_id==homework_id)
    return db(query).select(db.assignment_grade.grade)

def is_user_teacher(section_id):
    return db.membership(course_section=section_id,
                         role='teacher',
                         auth_user=auth.user.id)

def is_user_student(section_id):
    return db.membership(course_section=section_id,
                         role='student',
                         auth_user=auth.user.id)

def convert_to_list(hw):
    my_list=[]
    for d in hw:
        if d.grade >-1:
            my_list.append(d.grade)
        else:
            my_list.append(0)
    return my_list
