from flask import render_template, request, jsonify, Blueprint
from app import db
from app.models import Course, Instructor, Student

students_bp = Blueprint('students', __name__)  
courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

# === HTML Page Routes  For Students ===

@students_bp.route("/students", strict_slashes=False)
def student_list_page():
    return render_template("students/students_list.html")

@students_bp.route("/students/add", strict_slashes=False)
def add_student_page():
    return render_template("students/student_add.html")

@students_bp.route("/students/edit", strict_slashes=False)
def edit_student_page():
    return render_template("students/student_edit.html")

# === API Routes For Students===

# Get all students
@students_bp.route("/api/students", methods=["GET"], strict_slashes=False)
def get_all_students():
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

@students_bp.route("/instructors", strict_slashes=False)
def instructor_list_page():
    instructors = Instructor.query.all()
    return render_template("instructors/instructor_list.html", instructors=instructors)

@students_bp.route("/instructors/add", strict_slashes=False)
def instructor_add_page():
    return render_template("instructors/instructor_add.html")

@students_bp.route("/instructors/edit/<int:id>", strict_slashes=False)
def instructor_edit_page(id):
    instructor = Instructor.query.get_or_404(id)
    return render_template("instructors/instructor_edit.html", instructor=instructor)

# === API Routes For Instructors===

# GET: All instructors
@students_bp.route("/api/instructors", methods=["GET"], strict_slashes=False)
def get_all_instructors():
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
@students_bp.route("/api/instructors/<int:id>", methods=["GET"], strict_slashes=False)
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
@students_bp.route("/api/instructors", methods=["POST"], strict_slashes=False)
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
@students_bp.route("/api/instructors/<int:id>", methods=["PUT"], strict_slashes=False)
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
@students_bp.route("/api/instructors/<int:id>", methods=["DELETE"], strict_slashes=False)
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

@students_bp.route("/courses", strict_slashes=False)
def course_list_page():
    courses = Course.query.all()
    instructors = Instructor.query.all()
    return render_template("courses/courses_list.html", courses=courses, instructors=instructors)

@students_bp.route("/courses/add", strict_slashes=False)
def course_add_page():
    instructors = Instructor.query.all()
    return render_template("courses/course_add.html", instructors=instructors)

@students_bp.route("/courses/edit/<int:id>", strict_slashes=False)
def course_edit_page(id):
    course = Course.query.get_or_404(id)
    instructors = Instructor.query.all()
    return render_template("courses/course_edit.html", course=course, instructors=instructors)


# === API Routes For Courses===

from app.models import Course, Instructor  # En üstteki importlara ekle

# GET: All courses
@students_bp.route("/api/courses", methods=["GET"], strict_slashes=False)
def get_all_courses():
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
@students_bp.route("/api/courses/<int:id>", methods=["GET"], strict_slashes=False)
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
@students_bp.route("/api/courses", methods=["POST"], strict_slashes=False)
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
@students_bp.route("/api/courses/<int:id>", methods=["PUT"], strict_slashes=False)
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
@students_bp.route("/api/courses/<int:id>", methods=["DELETE"], strict_slashes=False)
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
