from app import create_app, db
from app.models import Course, Instructor

app = create_app()

with app.app_context():
    # ⚠️ Use an existing instructor_id from your DB
    default_instructor_id = 1  # change this to a real instructor ID

    course_list = [
        Course(code="CENG101", name="Introduction to Programming", credit=4, instructor_id=default_instructor_id),
        Course(code="CENG102", name="Programming II (Object-Oriented Programming)", credit=4, instructor_id=default_instructor_id),
        Course(code="CENG201", name="Data Structures and Algorithms", credit=4, instructor_id=default_instructor_id),
        Course(code="CENG202", name="Discrete Mathematics for Engineers", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG203", name="Digital Logic Design", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG204", name="Computer Organization", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG301", name="Operating Systems", credit=4, instructor_id=default_instructor_id),
        Course(code="CENG302", name="Database Management Systems", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG303", name="Computer Networks", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG304", name="Software Engineering", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG401", name="Artificial Intelligence", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG402", name="Machine Learning", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG403", name="Computer Architecture", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG404", name="Web Technologies", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG405", name="Embedded Systems", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG406", name="Information Security", credit=3, instructor_id=default_instructor_id),
        Course(code="CENG407", name="Graduation Project I", credit=2, instructor_id=default_instructor_id),
        Course(code="CENG408", name="Graduation Project II", credit=4, instructor_id=default_instructor_id),
    ]

    db.session.bulk_save_objects(course_list)
    db.session.commit()
    print("Computer Engineering courses added successfully.")
