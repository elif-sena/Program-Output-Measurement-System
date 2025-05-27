document.addEventListener("DOMContentLoaded", () => {
    loadCourses();
});

function loadCourses() {
    fetch("/api/courses")
        .then(response => response.json())
        .then(data => displayCourses(data))
        .catch(error => console.error("Error loading courses:", error));
}

function displayCourses(courses) {
    const tbody = document.getElementById("courseTableBody");
    tbody.innerHTML = "";

    courses.forEach(course => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${course.name}</td>
            <td>${course.code}</td>
            <td>${course.credit}</td>
            <td>${course.instructor}</td>
            <td>
                <a href="/courses/edit/${course.id}" class="btn btn-warning btn-sm">Edit</a>
                <button class="btn btn-danger btn-sm" onclick="deleteCourse(${course.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function applyFilters() {
    const nameQuery = document.getElementById("searchInput").value.toUpperCase().trim();
    const creditMin = parseInt(document.getElementById("minNumber").value) || 0;
    const creditMax = parseInt(document.getElementById("maxNumber").value) || Infinity;
    const firstLetter = document.getElementById("firstLetterFilter").value.toUpperCase();

    fetch("/api/courses")
        .then(response => response.json())
        .then(data => {
            const filtered = data.filter(course => {
                const name = course.name.toUpperCase();
                const instructor = course.instructor.toUpperCase();
                const credit = parseInt(course.credit);

                return (
                    credit >= creditMin &&
                    credit <= creditMax &&
                    (!nameQuery || name.includes(nameQuery)) &&
                    (!firstLetter || instructor.startsWith(firstLetter))
                );
            });
            displayCourses(filtered);
        })
        .catch(error => console.error("Error filtering courses:", error));
}

function deleteCourse(courseId) {
    if (!confirm("Are you sure you want to delete this course?")) return;

    fetch(`/api/courses/${courseId}`, {
        method: "DELETE"
    })
        .then(response => {
            if (response.ok) {
                alert("Course deleted successfully.");
                loadCourses();
            } else {
                alert("Failed to delete course.");
            }
        })
        .catch(error => console.error("Error deleting course:", error));
}
