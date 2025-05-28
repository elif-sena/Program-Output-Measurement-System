from app.models import CoursePOMap, Grade, ProgramOutcome


def calculate_student_po_success(student_id, passing_score=60):
    """
    Calculates the Program Outcome (PO) achievement for a given student ID.

    Returns:
        {
            "po_results": {
                "PO1": {"average_grade": 75, "passed": True},
                "PO2": {"average_grade": 55, "passed": False},
                ...
            },
            "overall_success_rate": 75.0
        }
    """
    from sqlalchemy import func

    # 1. Retrieve all grades of the student, including course_id and grade
    grades = Grade.query.filter_by(student_id=student_id).all()
    if not grades:
        # If no grades found, return empty result with 0 success rate
        return {"po_results": {}, "overall_success_rate": 0}

    # Dictionary to accumulate grades per PO code
    po_grades = {}

    # Loop through each grade the student received
    for grade in grades:
        # Find all POs mapped to the course of this grade
        course_pos = CoursePOMap.query.filter_by(course_id=grade.course_id).all()
        for mapping in course_pos:
            po_id = mapping.po_id
            po = ProgramOutcome.query.get(po_id)
            # Initialize list for PO if not present
            if po.code not in po_grades:
                po_grades[po.code] = []
            # Append the grade to the PO's grade list
            po_grades[po.code].append(grade.grade)

    po_results = {}
    passed_count = 0
    total_pos = len(po_grades)

    # Calculate average grade and pass status for each PO
    for po_code, grades_list in po_grades.items():
        avg_grade = sum(grades_list) / len(grades_list)
        passed = avg_grade >= passing_score
        po_results[po_code] = {
            "average_grade": round(avg_grade, 2),
            "passed": passed
        }
        if passed:
            passed_count += 1

    # Calculate overall success rate across all POs
    overall_success_rate = (passed_count / total_pos) * 100 if total_pos > 0 else 0

    return {
        "po_results": po_results,
        "overall_success_rate": round(overall_success_rate, 2)
    }

def calculate_overall_po_success(po_id, passing_score=60):
    """
    Calculates the overall success rate for a given Program Outcome (PO) across all students.

    Returns:
        {
            "po_code": "PO1",
            "po_description": "Description here",
            "average_grade": 72.5,
            "success_rate": 80.0,  # percentage of students who passed this PO
            "total_students": 50,
            "passed_students": 40
        }
    """
    from sqlalchemy import func

    # Get PO details
    po = ProgramOutcome.query.get(po_id)
    if not po:
        return None  # or raise Exception("PO not found")

    # Find all courses mapped to this PO
    course_mappings = CoursePOMap.query.filter_by(po_id=po_id).all()
    course_ids = [cm.course_id for cm in course_mappings]
    if not course_ids:
        return None  # No courses mapped to this PO

    # Find all grades in these courses
    grades = Grade.query.filter(Grade.course_id.in_(course_ids)).all()
    if not grades:
        return {
            "po_code": po.code,
            "po_description": po.description,
            "average_grade": 0,
            "success_rate": 0,
            "total_students": 0,
            "passed_students": 0
        }

    # Organize grades by student_id
    student_grades = {}
    for grade in grades:
        student_grades.setdefault(grade.student_id, []).append(grade.grade)

    total_students = len(student_grades)
    passed_students = 0
    total_avg_sum = 0

    # Calculate average grade per student and count who passed
    for grades_list in student_grades.values():
        avg_grade = sum(grades_list) / len(grades_list)
        total_avg_sum += avg_grade
        if avg_grade >= passing_score:
            passed_students += 1

    overall_avg = total_avg_sum / total_students if total_students > 0 else 0
    success_rate = (passed_students / total_students) * 100 if total_students > 0 else 0

    return {
        "po_code": po.code,
        "po_description": po.description,
        "average_grade": round(overall_avg, 2),
        "success_rate": round(success_rate, 2),
        "total_students": total_students,
        "passed_students": passed_students
    }
