document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("addStudentForm");

    form.addEventListener("submit", function (e) {
        e.preventDefault();     // Sayfanın yenilenmesini engelle

        // Formdaki değerleri al
        const firstName = document.getElementById("firstName").value.trim();
        const lastName = document.getElementById("lastName").value.trim();
        const studentNumber = parseInt(document.getElementById("studentNumber").value);
        const email = document.getElementById("email").value.trim();
        const phone = document.getElementById("phone").value.trim();

        // Basit validasyon
        if (!firstName || !lastName || !studentNumber || !email || !phone) {
            alert("Lütfen tüm zorunlu alanları doldurun.");
            return;
        }

        const newStudent = {
            first_name: firstName,
            last_name: lastName,
            student_number: studentNumber,
            email: email,
            phone: phone
        };

        fetch("/api/students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newStudent)
        })
            .then(response => {
                if (response.ok) {
                    alert("Student added successfully.");
                    // Kayıt başarılıysa liste sayfasına yönlendir:
                    window.location.href = "/students";
                }
                else {
                    alert("Failed to add student.");
                }
            })
            .catch(error => {
                console.error("Error adding student:", error);
            });
    });
});