document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addCourseForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const newCourse = {
            name: document.getElementById("courseName").value.trim(),
            code: document.getElementById("courseCode").value.trim(),
            credit: parseInt(document.getElementById("courseCredit").value),
            instructor: document.getElementById("instructor").value.trim()
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
