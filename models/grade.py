db.define_table(
    'class_assignment',
    Field('section_id', 'reference course_section'),
    Field('name'),
    Field('weight', 'float'),
    Field('total_points', 'integer'),
    Field('assignment_order', 'integer'),
    format = lambda class_assignment: class_assignment.section_id.name + ' - ' + class_assignment.name + ' - ' +str(class_assignment.total_points))

db.define_table(
    'grade',
    Field('grade_value', 'float'),
    Field('section_id', 'reference course_section'),
    Field('assignment_name', 'reference class_assignment'),
    Field('total_points', 'reference class_assignment'),
    Field('auth_user', 'reference auth_user'),
    Field('teacher_comment'))
