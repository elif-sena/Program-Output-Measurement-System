document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addCourseForm");

    const pathParts = window.location.pathname.split('/');
    const courseId = pathParts[pathParts.length - 1];

    // Kurs bilgilerini çek ve forma doldur
    fetch(`/api/courses/${courseId}`)
        .then(response => response.json())
        .then(course => {
            document.getElementById("courseName").value = course.name;
            document.getElementById("courseCode").value = course.code;
            document.getElementById("courseCredit").value = course.credit;
            document.getElementById("instructor").value = course.instructor;
        })
        .catch(error => {
            console.error("Error loading course:", error);
            alert("Failed to load course.");
        });

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const updatedCourse = {
            name: document.getElementById("courseName").value.trim(),
            code: document.getElementById("courseCode").value.trim(),
            credit: parseInt(document.getElementById("courseCredit").value),
            instructor: document.getElementById("instructor").value.trim()
        };

        fetch(`/api/courses/${courseId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedCourse)
        })
        .then(response => {
            if (response.ok) {
                alert("Course updated successfully.");
                window.location.href = "/courses";
            } else {
                alert("Failed to update course.");
            }
        })
        .catch(error => console.error("Error updating course:", error));
    });
});
