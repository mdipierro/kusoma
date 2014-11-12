# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def manage_grades():
    section_id=request.args(0, cast=int)
    
    if (is_user_teacher(section_id) or auth.user.is_administrator):
        redirect(URL('teacher',args=section_id))
    elif (is_user_student(section_id)):
        redirect(URL('student',args=section_id))
    else:
        session.flash = 'Not authorized'
        redirect(URL('default','index', args=section_id))

    return dict()

@auth.requires_login()
def teacher():
    section_id = request.args(0, cast=int)
    add_section_menu(section_id)
    if not (is_user_teacher(section_id)):
        session.flash = 'Not authorized'
        redirect(URL('default','index',args=section_id))

    response.files.insert(0,URL('static','js/jquery.js'))
    response.files.insert(0,URL('static','js/jquery.handsontable.full.js'))
    response.files.insert(0,URL('static','css/jquery.handsontable.full.css'))
    response.files.insert(0,URL('static','css/grading.css'))

    response.files.insert(0,URL('static','js/bootstrap-switch.min.js'))
    response.files.insert(0,URL('static','css/bootstrap-switch.min.css'))

    session.flash = 'Welcome Teacher'
    students = get_all_students(section_id)

    for st in students:
        st.hws = get_grades_student(section_id, st.auth_user.id)
        st.final = get_final_grade(section_id, st.auth_user.id).first()


    hws = get_homework_section(section_id)
    stat_options = get_statistics(section_id)
    stat_data=[]

    for hw in hws:
        s = convert_to_list(get_assignment_by_homework(section_id, hw.id))
        if s:
            mean = sum(s)/len(s)
            var = sum(x*x for x in s)/len(s) - mean**2
            stat_data.append({
                'min':round(min(s),2),
                'max':round(max(s),2),
                'average':round(mean,2),
                'median':round(sorted(s)[int(len(s)/2)],2),
                'mean':round(mean,2),
                'sum':round(sum(s),2),
                'cov':round(0.0,2), # not well defined
                'var':round(var,2),
                'std':round(var**0.5,2),
                'hw':hw
            })
    return dict(section_id=section_id, users=students, names=students.first().hws,stat = stat_data, stat_options=stat_options)

@auth.requires_login()
def student():
    section_id = request.args(0, cast=int)
    add_section_menu(section_id)
    if not (is_user_student(section_id)):
        session.flash = 'Not authorized'
        redirect(URL('default','index',args=section_id))
    session.flash = "Welcome %s %s" % (auth.user.first_name, auth.user.last_name)
    section = db.course_section(section_id)
    student_grades = get_grades_student(section_id, auth.user.id)
    grade_record = get_final_grade(section_id, auth.user.id)
    hws = get_homework_section(section_id)

    stat_options = get_statistics(section_id)
    stat_data=[]

    for hw in hws:
        s = convert_to_list(get_assignment_by_homework(section_id, hw.id))
        if s:

            mean = sum(s)/len(s)
            var = sum(x*x for x in s)/len(s) - mean**2
            stat_data.append({
                'min':round(min(s),2),
                'max':round(max(s),2),
                'average':round(mean,2),
                'median':round(sorted(s)[int(len(s)/2)],2),
                'mean':round(mean,2),
                'sum':round(sum(s),2),
                'cov':round(0.0,2), # not well defined
                'var':round(var,2),
                'std':round(var**0.5,2),
                'hw':hw
            })

    return dict(student_grades=student_grades, section=section, stat=stat_data, grade_record=grade_record, stat_options=stat_options)

@auth.requires_login()
def savedata():
    import gluon.contrib.simplejson
    students = gluon.contrib.simplejson.loads(request.body.read())
    section_id = request.args(0, cast=int)
    hws = get_homework_section(section_id)
    for student in students['data']:
        id=student['id']
        final = student['final']
        comment = student['comment']
        db.course_grade.update_or_insert((db.course_grade.section_id==section_id) &(db.course_grade.auth_user==id),section_id=section_id,auth_user=id,grade=final,teacher_comment=comment)

        for hw in hws:
            homeworks = student["hw"]
            grade = homeworks[str(hw.id)]

            if grade > -1:
                db.assignment_grade.update_or_insert((db.assignment_grade.section_id==section_id)&(db.assignment_grade.assignment_id==hw.id)&(db.assignment_grade.user_id==id),section_id=section_id, assignment_id=hw.id, user_id=id, grade=grade, assignment_comment='')
            pass

    session.flash = "Grades Saved"
    return response.json(students)

def statistics():
    section_id = request.args(0, cast=int)
    stat = request.vars['stat']
    value = request.vars['val']

    if(stat == "min"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             min_score=value)
    if(stat == "max"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             max_score=value)
    if(stat == "avg"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             avg_score=value)
    if(stat == "med"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             median_score=value)
    if(stat == "mea"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             mean_score=value)
    if(stat == "sum"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             sum_score=value)
    if(stat == "cov"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             cov=value)
    if(stat == "var"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             var=value)
    if(stat == "std"):
        db.section_statistics.update_or_insert(db.section_statistics.section_id==section_id, section_id =section_id,
             std=value)

    session.flash = "Statistics Options Changed"
    return str(section_id)  + " " + stat + " " +value

@auth.requires_login()
def addhw():
    grid = SQLFORM.smartgrid(db.homework)
    return dict(grid=grid)

@auth.requires_login()
def addgrade():
    grid = SQLFORM.smartgrid(db.assignment_grade)
    return dict(grid=grid)
