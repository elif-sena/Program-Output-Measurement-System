document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addInstructorForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const newInstructor = {
            name: document.getElementById("name").value.trim(),
            title: document.getElementById("title").value,
            email: document.getElementById("email").value.trim()
        };

        fetch("/api/instructors", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newInstructor)
        })
        .then(response => {
            if (response.ok) {
                alert("Instructor added successfully.");
                window.location.href = "/instructors";
            } else {
                alert("Failed to add instructor.");
            }
        })
        .catch(error => console.error("Error adding instructor:", error));
    });
});
