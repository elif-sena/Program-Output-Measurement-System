from flask import render_template, request, jsonify, Blueprint, session
from sqlalchemy import func
from app import db
from app.models import Course, CoursePOMap, Grade, Instructor, ProgramOutcome, Student
import pandas as pd
from flask import request, redirect, url_for, flash, render_template
from app.po_calculations import calculate_overall_po_success


students_bp = Blueprint('students', __name__)  
courses_bp = Blueprint('courses', __name__)
auth_bp = Blueprint('auth', __name__)
grades_bp = Blueprint('grades', __name__)
instructors_bp = Blueprint('instructors', __name__)


# === HTML Pages For Login And Dashboard===

@auth_bp.route("/login", methods=["GET"], strict_slashes=False)
def login_page():
    return render_template("auth/login.html")

@auth_bp.route("/dashboard", methods=["GET"], strict_slashes=False)
def dashboard_page():
    total_students = Student.query.count()
    total_instructors = Instructor.query.count()
    total_courses = Course.query.count()
    return render_template("dashboard.html", total_students=total_students,
                           total_instructors=total_instructors, total_courses=total_courses)

# === API Routes For Login And Dashboard ===

@auth_bp.route("/api/login", methods=["POST"], strict_slashes=False)
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = Instructor.query.filter_by(email=email).first()
    if user and password == "admin123":  # Güvenli değil, sadece örnek
        session["user_id"] = user.id
        session["user_name"] = user.name
        return jsonify({"message": "Login successful!"})
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/logout", strict_slashes=False)
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"})

# === HTML Page Routes  For Students ===

@students_bp.route("/students", strict_slashes=False)
def student_list_page():
    return render_template("students/student_list.html")

@students_bp.route("/students/add", strict_slashes=False)
def add_student_page():
    return render_template("students/student_add.html")

@students_bp.route("/students/edit", strict_slashes=False)
def edit_student_page():
    return render_template("students/student_edit.html")

from flask import render_template, request
from sqlalchemy import func

@students_bp.route('/students/charts')
def student_charts():
    student_id = request.args.get('student_id', type=int)
    if not student_id:
        return "Student ID is required", 400

    # Average grade per course
    course_averages = (
        db.session.query(
            Course.code.label('course_code'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Grade, Grade.course_id == Course.id)
        .filter(Grade.student_id == student_id)
        .group_by(Course.id)
        .all()
    )

    # Average grade per program outcome
    # Join CoursePOMap to link courses with program outcomes
    po_averages = (
        db.session.query(
            ProgramOutcome.code.label('po_code'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(CoursePOMap, CoursePOMap.po_id == ProgramOutcome.id)
        .join(Course, Course.id == CoursePOMap.course_id)
        .join(Grade, (Grade.course_id == Course.id) & (Grade.student_id == student_id))
        .group_by(ProgramOutcome.id)
        .all()
    )

    return render_template('/students/student_charts.html',
                           course_averages=course_averages,
                           po_averages=po_averages)

    student_id = request.args.get('student_id', type=int)
    if not student_id:
        return "Student ID is required", 400

    student = Student.query.get(student_id)
    if not student:
        return "Student not found", 404

    course_averages = (
        Grade.query
        .with_entities(Course.code.label('course_code'), func.avg(Grade.grade).label('avg_grade'))
        .join(Course, Grade.course_id == Course.id)
        .filter(Grade.student_id == student_id)
        .group_by(Course.id)
        .all()
    )

    po_averages = (
        db.session.query(
            ProgramOutcome.code.label('po_code'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(CoursePOMap, ProgramOutcome.id == CoursePOMap.po_id)
        .join(Course, CoursePOMap.course_id == Course.id)
        .join(Grade, (Grade.course_id == Course.id) & (Grade.student_id == student_id))
        .group_by(ProgramOutcome.id)
        .all()
    )

    # convert to serializable format
    course_averages = [{'course_code': c.course_code, 'avg_grade': float(c.avg_grade)} for c in course_averages]
    po_averages = [{'po_code': p.po_code, 'avg_grade': float(p.avg_grade)} for p in po_averages]

    # create serializable student dict
    student_data = {
        'first_name': student.first_name,
        'last_name': student.last_name,
        'student_number': student.student_number,
        'email': student.email,
        'phone': student.phone,
    }

    return render_template('students/student_charts.html',
                           student=student_data,
                           course_averages=course_averages,
                           po_averages=po_averages)

    student_id = request.args.get('student_id', type=int)
    if not student_id:
        return "Student ID is required", 400

    # Fetch student info
    student = Student.query.get(student_id)
    if not student:
        return "Student not found", 404

    # Average grade per course
    course_averages = (
        Grade.query
        .with_entities(Course.code.label('course_code'), func.avg(Grade.grade).label('avg_grade'))
        .join(Course, Grade.course_id == Course.id)
        .filter(Grade.student_id == student_id)
        .group_by(Course.id)
        .all()
    )

    # Average grade per program outcome
    # Join Grade -> Course -> CoursePOMap -> ProgramOutcome
    po_averages = (
        db.session.query(
            ProgramOutcome.code.label('po_code'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(CoursePOMap, ProgramOutcome.id == CoursePOMap.po_id)
        .join(Course, CoursePOMap.course_id == Course.id)
        .join(Grade, (Grade.course_id == Course.id) & (Grade.student_id == student_id))
        .group_by(ProgramOutcome.id)
        .all()
    )

    # Convert to list of dict for JSON serialization
    course_averages = [{'course_code': c.course_code, 'avg_grade': float(c.avg_grade)} for c in course_averages]
    po_averages = [{'po_code': p.po_code, 'avg_grade': float(p.avg_grade)} for p in po_averages]

    return render_template('students/student_charts.html',
                           student=student,
                           course_averages=course_averages,
                           po_averages=po_averages)


    student_id = request.args.get('student_id', type=int)
    if not student_id:
        return "Student ID is required", 400

    # Get student info
    student = Student.query.get(student_id)
    if not student:
        return "Student not found", 404

    # Average grade per course
    course_averages = (
        db.session.query(
            Course.code.label('course_code'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Grade, Grade.course_id == Course.id)
        .filter(Grade.student_id == student_id)
        .group_by(Course.id)
        .all()
    )

    # Average grade per program outcome
    po_averages = (
        db.session.query(
            ProgramOutcome.code.label('po_code'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(CoursePOMap, CoursePOMap.po_id == ProgramOutcome.id)
        .join(Course, Course.id == CoursePOMap.course_id)
        .join(Grade, (Grade.course_id == Course.id) & (Grade.student_id == student_id))
        .group_by(ProgramOutcome.id)
        .all()
    )

    return render_template('/students/student_charts.html',
                           student=student,
                           course_averages=course_averages,
                           po_averages=po_averages)


# === API Routes For Students===
# Get all students
@students_bp.route("/api/students", methods=["GET"], strict_slashes=False)
def list_students():
    students = Student.query.all()
    return jsonify([
        {
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "student_number": s.student_number,
            "email": s.email,
            "phone": s.phone
        }
        for s in students
    ])

# Get a single student by ID
@students_bp.route("/api/students/<int:id>", methods=["GET"], strict_slashes=False)
def get_student(id):
    student = Student.query.get(id)
    if student:
        return jsonify({
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "student_number": student.student_number,
            "email": student.email,
            "phone": student.phone
        })
    return jsonify({"error": "Student not found"}), 404

# Add a new student
@students_bp.route("/api/students", methods=["POST"], strict_slashes=False)
def add_student():
    data = request.get_json()
    try:
        new_student = Student(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            student_number=data.get("student_number"),
            email=data.get("email"),
            phone=data.get("phone")
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Student added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update existing student
@students_bp.route("/api/students/<int:id>", methods=["PUT"], strict_slashes=False)
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    try:
        student.first_name = data.get("first_name")
        student.last_name = data.get("last_name")
        student.student_number = data.get("student_number")
        student.email = data.get("email")
        student.phone = data.get("phone")

        db.session.commit()
        return jsonify({"message": "Student updated successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete student
@students_bp.route("/api/students/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# === HTML Page Routes  For Instructors ===

@instructors_bp.route("/instructors", strict_slashes=False)
def instructor_list_page():
    instructors = Instructor.query.all()
    return render_template("instructors/instructor_list.html", instructors=instructors)

@instructors_bp.route("/instructors/add", strict_slashes=False)
def instructor_add_page():
    return render_template("instructors/instructor_add.html")

@instructors_bp.route("/instructors/edit/<int:id>", strict_slashes=False)
def instructor_edit_page(id):
    instructor = Instructor.query.get_or_404(id)
    return render_template("instructors/instructor_edit.html", instructor=instructor)

# === API Routes For Instructors===

# GET: All instructors
@instructors_bp.route("/api/instructors", methods=["GET"], strict_slashes=False)
def list_instructors():
    instructors = Instructor.query.all()
    return jsonify([
        {
            "id": i.id,
            "name": i.name,
            "title": i.title,
            "email": i.email
        }
        for i in instructors
    ])

# GET: Single instructor
@instructors_bp.route("/api/instructors/<int:id>", methods=["GET"], strict_slashes=False)
def get_instructor(id):
    instructor = Instructor.query.get(id)
    if not instructor:
        return jsonify({"error": "Instructor not found"}), 404
    return jsonify({
        "id": instructor.id,
        "name": instructor.name,
        "title": instructor.title,
        "email": instructor.email
    })

# POST: Add instructor
@instructors_bp.route("/api/instructors", methods=["POST"], strict_slashes=False)
def add_instructor():
    data = request.get_json()
    try:
        instructor = Instructor(
            name=data.get("name"),
            title=data.get("title"),
            email=data.get("email")
        )
        db.session.add(instructor)
        db.session.commit()
        return jsonify({"message": "Instructor added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# PUT: Update instructor
@instructors_bp.route("/api/instructors/<int:id>", methods=["PUT"], strict_slashes=False)
def update_instructor(id):
    instructor = Instructor.query.get(id)
    if not instructor:
        return jsonify({"error": "Instructor not found"}), 404

    data = request.get_json()
    try:
        instructor.name = data.get("name")
        instructor.title = data.get("title")
        instructor.email = data.get("email")

        db.session.commit()
        return jsonify({"message": "Instructor updated successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# DELETE: Instructor
@instructors_bp.route("/api/instructors/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete_instructor(id):
    instructor = Instructor.query.get(id)
    if not instructor:
        return jsonify({"error": "Instructor not found"}), 404

    try:
        db.session.delete(instructor)
        db.session.commit()
        return jsonify({"message": "Instructor deleted successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# === HTML Page Routes  For Courses ===

@courses_bp.route("/courses", strict_slashes=False)
def cource_list_page():
    courses = Course.query.all()
    instructors = Instructor.query.all()
    return render_template("courses/course_list.html", courses=courses, instructors=instructors)

@courses_bp.route("/courses/add", strict_slashes=False)
def course_add_page():
    instructors = Instructor.query.all()
    return render_template("courses/course_add.html", instructors=instructors)

@courses_bp.route("/courses/edit/<int:id>", strict_slashes=False)
def course_edit_page(id):
    course = Course.query.get_or_404(id)
    instructors = Instructor.query.all()
    return render_template("courses/course_edit.html", course=course, instructors=instructors)


# === API Routes For Courses===

from app.models import Course, Instructor  # En üstteki importlara ekle

# GET: All courses
@courses_bp.route("/api/courses", methods=["GET"], strict_slashes=False)
def list_courses():
    courses = Course.query.all()
    return jsonify([
        {
            "id": c.id,
            "code": c.code,
            "name": c.name,
            "credit": c.credit,
            "instructor": c.instructor.name if c.instructor else None
        }
        for c in courses
    ])

# GET: Single course
@courses_bp.route("/api/courses/<int:id>", methods=["GET"], strict_slashes=False)
def get_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify({
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "credit": course.credit,
        "instructor_id": course.instructor_id
    })

# POST: Add course
@courses_bp.route("/api/courses", methods=["POST"], strict_slashes=False)
def add_course():
    data = request.get_json()
    try:
        course = Course(
            code=data.get("code"),
            name=data.get("name"),
            credit=data.get("credit"),
            instructor_id=data.get("instructor_id")
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({"message": "Course added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# PUT: Update course
@courses_bp.route("/api/courses/<int:id>", methods=["PUT"], strict_slashes=False)
def update_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    data = request.get_json()
    try:
        course.code = data.get("code")
        course.name = data.get("name")
        course.credit = data.get("credit")
        course.instructor_id = data.get("instructor_id")

        db.session.commit()
        return jsonify({"message": "Course updated successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# DELETE: Course
@courses_bp.route("/api/courses/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
# === HTML Pages For Grades ===

@grades_bp.route("/grades", strict_slashes=False)
def grade_list_page():
    grades = Grade.query.all()
    return render_template("grades/grade_list.html", grades=grades)

@grades_bp.route("/grades/upload", strict_slashes=False)
def add_grade_page():
    students = Student.query.all()
    courses = Course.query.all()
    return render_template("grades/upload_grades.html", students=students, courses=courses)

@grades_bp.route('/grades/report')
def report_dashboard():
    return render_template('grades/grade_report.html')

# === API Routes For Grades ===

@grades_bp.route("/api/grades", methods=["GET"], strict_slashes=False)
def list_grades():
    grades = Grade.query.all()
    return jsonify([
        {
            "id": g.id,
            "student_id": g.student_id,
            "course_id": g.course_id,
            "grade": g.grade,
            "student_name": g.student.first_name + " " + g.student.last_name,
            "course_name": g.course.name
        }
        for g in grades
    ])

@grades_bp.route("/api/grades/<int:id>", methods=["GET"], strict_slashes=False)
def get_grade(id):
    grade = Grade.query.get(id)
    if not grade:
        return jsonify({"error": "Grade not found"}), 404
    return jsonify({
        "id": grade.id,
        "student_id": grade.student_id,
        "course_id": grade.course_id,
        "grade": grade.grade
    })

@grades_bp.route("/grades/upload", methods=["GET", "POST"])
def upload_grades_bulk():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return render_template("grades/upload_grades.html", error="No file uploaded")
        
        try:
            # Read file depending on extension
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                return render_template("grades/upload_grades.html", error="Invalid file format")

            # Check required columns
            required_cols = {"student_number", "course_code", "grade"}
            if not required_cols.issubset(set(df.columns.str.lower())):
                return render_template("grades/upload_grades.html", error="File must contain columns: student_number, course_code, grade")

            # Normalize columns to lowercase for safety
            df.columns = df.columns.str.lower()

            added_count = 0
            errors = []
            for _, row in df.iterrows():
                student = Student.query.filter_by(student_number=row['student_number']).first()
                course = Course.query.filter_by(code=row['course_code']).first()
                grade_val = row['grade']

                if not student:
                    errors.append(f"Student not found: {row['student_number']}")
                    continue
                if not course:
                    errors.append(f"Course not found: {row['course_code']}")
                    continue

                # Check if grade already exists for this student and course
                existing_grade = Grade.query.filter_by(student_id=student.id, course_id=course.id).first()
                if existing_grade:
                    # If you want to skip or update existing, decide here; skipping for now
                    errors.append(f"Grade already exists for {student.student_number} in {course.code}")
                    continue
                
                new_grade = Grade(student_id=student.id, course_id=course.id, grade=grade_val)
                db.session.add(new_grade)
                added_count += 1
            
            db.session.commit()
            
            message = f"Successfully added {added_count} grades."
            if errors:
                message += " Some entries skipped: " + "; ".join(errors)
            return render_template("grades/upload_grades.html", message=message)

        except Exception as e:
            db.session.rollback()
            return render_template("grades/upload_grades.html", error=f"Error processing file: {str(e)}")
    
    # GET request shows the upload form
    return render_template("grades/upload_grades.html")

@grades_bp.route("/grades/delete/<int:id>", methods=["POST"])
def delete_grade(id):
    grade = Grade.query.get_or_404(id)
    try:
        db.session.delete(grade)
        db.session.commit()
        flash("Grade deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting grade: {str(e)}", "danger")
    return redirect(url_for('grades_bp.grade_list_page'))

@grades_bp.route('/grades/api/average_grades_by_po')
def average_grades_by_po():
    po_list = ProgramOutcome.query.all()

    results = []
    for po in po_list:
        po_stats = calculate_overall_po_success(po.id)
        if po_stats:
            results.append(po_stats)

   
    data = {
        "labels": [r["po_code"] for r in results],
        "averages": [r["average_grade"] for r in results],
       
        "success_rates": [r["success_rate"] for r in results]
    }
    return jsonify(data)


@grades_bp.route('/grades/api/average_grades_all_students_per_course')
def average_grades_all_students_per_course():
 
    results = db.session.query(
        Course.code,
        func.avg(Grade.grade).label('avg_grade')
    ).join(Grade.course).group_by(Course.id).all()

    data = {
        "labels": [r[0] for r in results],
        "averages": [round(r[1], 2) for r in results]
    }
    return jsonify(data)