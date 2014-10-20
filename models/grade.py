db.define_table(
    'class_assignment',
    Field('section_id', 'reference course_section'),
    Field('name'),
    Field('weight'),
    Field('assignment_order'),
    format = lambda class_assignment: class_assignment.section_id.name + ' - ' + class_assignment.name )

db.define_table(
    'grade',
         Field('grade_value'),
         Field('section_id', 'reference course_section'),
         Field('assignment_name', 'reference class_assignment'),
         Field('auth_user', 'reference auth_user'))
