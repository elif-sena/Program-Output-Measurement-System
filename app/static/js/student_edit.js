document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("editStudentForm");

    // URL'den öğrenci id'sini al
    const urlParams = new URLSearchParams(window.location.search);
    const studentId = urlParams.get("id");

    if (!studentId) {
        alert("No student selected.");
        window.location.href = "/students";
    }



    // Var olan bilgiyi çekip doldur
    fetch(`/api/students/${studentId}`)
        .then(response => response.json())
        .then(student => {
            document.getElementById("firstName").value = student.first_name;
            document.getElementById("lastName").value = student.last_name;
            document.getElementById("studentNumber").value = student.student_number;
            document.getElementById("email").value = student.email;
            document.getElementById("phone").value = student.phone;
        })
        .catch(error => {
            console.error("Error loading student:", error);
        });

    // Güncelleme işlemi
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const updatedStudent = {
            first_name: document.getElementById("firstName").value.trim(),
            last_name: document.getElementById("lastName").value.trim(),
            student_number: parseInt(document.getElementById("studentNumber").value),
            email: document.getElementById("email").value.trim(),
            phone: document.getElementById("phone").value.trim()
        };

        fetch(`/api/students/${studentId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedStudent)
        })
            .then(response => {
                if (response.ok) {
                    alert("Student updated successfully.");
                    window.location.href = "/students";
                } else {
                    alert("Failed to update student.");
                }
            })
            .catch(error => {
                console.error("Error updating student:", error);
            });
    });
});
