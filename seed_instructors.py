from app import create_app, db
from app.models import Instructor

app = create_app()

with app.app_context():
    instructors = [
        Instructor(name="John Smith", title="Professor", email="john.smith@example.com"),
        Instructor(name="Jane Doe", title="Associate Professor", email="jane.doe@example.com"),
        Instructor(name="Emily Johnson", title="Lecturer", email="emily.johnson@example.com"),
        Instructor(name="Michael Brown", title="Senior Lecturer", email="michael.brown@example.com"),
        Instructor(name="Laura Wilson", title="Assistant Professor", email="laura.wilson@example.com"),
    ]

    db.session.bulk_save_objects(instructors)
    db.session.commit()

    print("5 instructors have been added successfully.")
