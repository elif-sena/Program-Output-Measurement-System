document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addCourseForm");
    const instructorSelect = document.getElementById("instructorSelect");

    // Öğretmenleri çek
    fetch("/api/instructors")
        .then(res => res.json())
        .then(instructors => {
            instructors.forEach(inst => {
                const option = document.createElement("option");
                option.value = inst.id;
                option.textContent = inst.name;
                instructorSelect.appendChild(option);
            });
        })
        .catch(err => {
            console.error("Error loading instructors:", err);
            alert("Failed to load instructors");
        });

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const newCourse = {
            name: document.getElementById("courseName").value.trim(),
            code: document.getElementById("courseCode").value.trim(),
            credit: parseInt(document.getElementById("courseCredit").value),
            instructor_id: parseInt(instructorSelect.value)
        };

        fetch("/api/courses", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newCourse)
        })
        .then(response => {
            if (response.ok) {
                alert("Course added successfully.");
                window.location.href = "/courses";
            } else {
                alert("Failed to add course.");
            }
        })
        .catch(error => console.error("Error adding course:", error));
    });
});
