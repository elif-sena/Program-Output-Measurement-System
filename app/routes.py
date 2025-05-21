from flask import render_template, request, jsonify, Blueprint
from app import db
from app.models import Student

students_bp = Blueprint('students', __name__)  

# === HTML Page Routes ===

@students_bp.route("/students", strict_slashes=False)
def student_list_page():
    return render_template("students/students_list.html")

@students_bp.route("/students/add", strict_slashes=False)
def add_student_page():
    return render_template("students/student_add.html")

@students_bp.route("/students/edit", strict_slashes=False)
def edit_student_page():
    return render_template("students/student_edit.html")

# === API Routes ===

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
