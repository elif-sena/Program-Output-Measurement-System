from app import create_app, db
from app.models import ProgramOutcome

app = create_app()

with app.app_context():
    # Program Outcomes
    po_list = [
        ProgramOutcome(code="PO1", description="Apply knowledge of mathematics, science, and engineering."),
        ProgramOutcome(code="PO2", description="Design and conduct experiments, analyze and interpret data."),
        ProgramOutcome(code="PO3", description="Design a system, component, or process to meet desired needs."),
        ProgramOutcome(code="PO4", description="Function on multidisciplinary teams."),
        ProgramOutcome(code="PO5", description="Identify, formulate, and solve engineering problems."),
        ProgramOutcome(code="PO6", description="Understand professional and ethical responsibility."),
        ProgramOutcome(code="PO7", description="Communicate effectively."),
        ProgramOutcome(code="PO8", description="Understand the impact of engineering solutions in a global, economic, environmental, and societal context."),
        ProgramOutcome(code="PO9", description="Engage in life-long learning."),
        ProgramOutcome(code="PO10", description="Be knowledgeable of contemporary issues."),
        ProgramOutcome(code="PO11", description="Use modern engineering tools necessary for engineering practice."),
    ]

    db.session.bulk_save_objects(po_list)
    db.session.commit()
    print("Program Outcomes have been added successfully.")
