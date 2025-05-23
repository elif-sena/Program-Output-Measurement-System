from app import create_app, db
from app.models import CoursePOMap

app = create_app()

with app.app_context():
    mappings = [
        # CENG101 - Introduction to Programming
        CoursePOMap(course_id=1, po_id=1),  # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=1, po_id=3),  # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=1, po_id=7),  # PO7: Communicate effectively.
        CoursePOMap(course_id=1, po_id=11), # PO11: Use modern engineering tools necessary for engineering practice.

        # CENG102 - Programming II (Object-Oriented Programming)
        CoursePOMap(course_id=2, po_id=1),  # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=2, po_id=3),  # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=2, po_id=7),  # PO7: Communicate effectively.
        CoursePOMap(course_id=2, po_id=11), # PO11: Use modern engineering tools necessary for engineering practice.

        # CENG201 - Data Structures and Algorithms
        CoursePOMap(course_id=3, po_id=1),  # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=3, po_id=3),  # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=3, po_id=5),  # PO5: Identify, formulate, and solve engineering problems.
        CoursePOMap(course_id=3, po_id=11), # PO11: Use modern engineering tools necessary for engineering practice.

        # CENG202 - Discrete Mathematics for Engineers
        CoursePOMap(course_id=4, po_id=1),  # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=4, po_id=5),  # PO5: Identify, formulate, and solve engineering problems.

        # CENG203 - Digital Logic Design
        CoursePOMap(course_id=5, po_id=1),  # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=5, po_id=3),  # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=5, po_id=11), # PO11: Use modern engineering tools necessary for engineering practice.

        # CENG204 - Computer Organization
        CoursePOMap(course_id=6, po_id=1),  # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=6, po_id=3),  # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=6, po_id=11), # PO11: Use modern engineering tools necessary for engineering practice.

        # CENG301 - Operating Systems
        CoursePOMap(course_id=7, po_id=3),  # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=7, po_id=5),  # PO5: Identify, formulate, and solve engineering problems.
        CoursePOMap(course_id=7, po_id=6),  # PO6: Understand professional and ethical responsibility.
        CoursePOMap(course_id=7, po_id=11), # PO11: Use modern engineering tools necessary for engineering practice.

        # CENG302 - Database Management Systems
        CoursePOMap(course_id=8, po_id=3),  # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=8, po_id=7),  # PO7: Communicate effectively.
        CoursePOMap(course_id=8, po_id=11), # PO11: Use modern engineering tools necessary for engineering practice.

        # CENG303 - Computer Networks
        CoursePOMap(course_id=9, po_id=3),  # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=9, po_id=7),  # PO7: Communicate effectively.
        CoursePOMap(course_id=9, po_id=8),  # PO8: Understand the impact of engineering solutions in a global, economic, environmental, and societal context.

        # CENG304 - Software Engineering
        CoursePOMap(course_id=10, po_id=3), # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=10, po_id=4), # PO4: Function on multidisciplinary teams.
        CoursePOMap(course_id=10, po_id=7), # PO7: Communicate effectively.
        CoursePOMap(course_id=10, po_id=6), # PO6: Understand professional and ethical responsibility.

        # CENG401 - Artificial Intelligence
        CoursePOMap(course_id=11, po_id=1), # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=11, po_id=3), # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=11, po_id=9), # PO9: Engage in life-long learning.
        CoursePOMap(course_id=11, po_id=11),# PO11: Use modern engineering tools necessary for engineering practice.

        # CENG402 - Machine Learning
        CoursePOMap(course_id=12, po_id=1), # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=12, po_id=3), # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=12, po_id=9), # PO9: Engage in life-long learning.
        CoursePOMap(course_id=12, po_id=11),# PO11: Use modern engineering tools necessary for engineering practice.

        # CENG403 - Computer Architecture
        CoursePOMap(course_id=13, po_id=1), # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=13, po_id=3), # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=13, po_id=11),# PO11: Use modern engineering tools necessary for engineering practice.

        # CENG404 - Web Technologies
        CoursePOMap(course_id=14, po_id=3), # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=14, po_id=7), # PO7: Communicate effectively.
        CoursePOMap(course_id=14, po_id=11),# PO11: Use modern engineering tools necessary for engineering practice.

        # CENG405 - Embedded Systems
        CoursePOMap(course_id=15, po_id=1), # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=15, po_id=3), # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=15, po_id=11),# PO11: Use modern engineering tools necessary for engineering practice.

        # CENG406 - Information Security
        CoursePOMap(course_id=16, po_id=1), # PO1: Apply knowledge of mathematics, science, and engineering.
        CoursePOMap(course_id=16, po_id=6), # PO6: Understand professional and ethical responsibility.
        CoursePOMap(course_id=16, po_id=8), # PO8: Understand the impact of engineering solutions in a global, economic, environmental, and societal context.

        # CENG407 - Graduation Project I
        CoursePOMap(course_id=17, po_id=3), # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=17, po_id=4), # PO4: Function on multidisciplinary teams.
        CoursePOMap(course_id=17, po_id=5), # PO5: Identify, formulate, and solve engineering problems.
        CoursePOMap(course_id=17, po_id=6), # PO6: Understand professional and ethical responsibility.
        CoursePOMap(course_id=17, po_id=7), # PO7: Communicate effectively.

        # CENG408 - Graduation Project II
        CoursePOMap(course_id=18, po_id=3), # PO3: Design a system, component, or process to meet desired needs.
        CoursePOMap(course_id=18, po_id=4), # PO4: Function on multidisciplinary teams.
        CoursePOMap(course_id=18, po_id=5), # PO5: Identify, formulate, and solve engineering problems.
        CoursePOMap(course_id=18, po_id=6), # PO6: Understand professional and ethical responsibility.
        CoursePOMap(course_id=18, po_id=7), # PO7: Communicate effectively.
        CoursePOMap(course_id=18, po_id=9), # PO9: Engage in life-long learning.
    ]

    db.session.bulk_save_objects(mappings)
    db.session.commit()
    print("Course-Program Outcome mappings added successfully.")
