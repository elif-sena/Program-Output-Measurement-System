document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("editInstructorForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const id = document.getElementById("instructorId").value;
        const updatedInstructor = {
            name: document.getElementById("name").value.trim(),
            title: document.getElementById("title").value,
            email: document.getElementById("email").value.trim()
        };

        fetch(`/api/instructors/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedInstructor)
        })
        .then(response => {
            if (response.ok) {
                alert("Instructor updated successfully.");
                window.location.href = "/instructors";
            } else {
                alert("Failed to update instructor.");
            }
        })
        .catch(error => {
            console.error("Error updating instructor:", error);
            alert("An error occurred while updating instructor.");
        });
    });
});
