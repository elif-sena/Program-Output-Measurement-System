document.addEventListener("DOMContentLoaded", function () {
    loadStudents();
});

// Tüm öğrencileri listeleyen fonksiyon
function loadStudents() {
    fetch("/api/students")  // Flask tarafındaki API endpoint
        .then(response => response.json())
        .then(data => {
            displayStudents(data);
        })
        .catch(error => {
            console.error("Error fetching students:", error);
        });
}

function displayStudents(students) {
    const tableBody = document.getElementById("studentTableBody");
    tableBody.innerHTML = ""; 

    students.forEach(student => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${parseInt(student.student_number)}</td>
            <td>${student.first_name}</td>
            <td>${student.last_name}</td>
            <td>${student.email}</td>
            <td>${student.phone}</td>
            <td>
                <a href="/students/edit?id=${student.id}" class="btn btn-warning btn-sm">Edit</a>
                <button class="btn btn-danger btn-sm" onclick="deleteStudent(${student.id})">Delete</button>
            </td>
        `;

        tableBody.appendChild(row);
    });
}


function applyFilters() {
    const numberMin = parseInt(document.getElementById("minNumber").value) || 0;
    const numberMax = parseInt(document.getElementById("maxNumber").value) || Infinity;
    const firstLetter = document.getElementById("firstLetterFilter").value.toUpperCase();
    const searchQuery = document.getElementById("searchInput").value.toUpperCase().trim();

    fetch("/api/students")
        .then(response => response.json())
        .then(data => {
            const filteredStudents = data.filter(student => {
                const num = parseInt(student.student_number);
                const firstName = student.first_name.toUpperCase();
                const lastName = student.last_name.toUpperCase();
                const fullName = `${firstName} ${lastName}`;

                let visible = true;

                // Numara aralığı filtresi
                if (isNaN(num) || num < numberMin || num > numberMax) visible = false;

                // Baş harf filtresi (sadece isimde)
                if (firstLetter && !firstName.startsWith(firstLetter)) visible = false;

                // Ad-soyad veya birleşik ad-soyad araması
                if (
                    searchQuery &&
                    !(
                        firstName.includes(searchQuery) ||
                        lastName.includes(searchQuery) ||
                        fullName.includes(searchQuery)
                    )
                ) {
                    visible = false;
                }

                return visible;
            });

            displayStudents(filteredStudents);
        })
        .catch(error => {
            console.error("Error filtering students:", error);
        });
}

// Silme işlemi
function deleteStudent(studentId) {
    if (!confirm("Are you sure you want to delete this student?")) return;

    fetch(`/api/students/${studentId}`, {
        method: "DELETE"
    })
        .then(response => {
            if (response.ok) {
                alert("Student deleted successfully.");
                loadStudents();
            } else {
                alert("Failed to delete student.");
            }
        })
        .catch(error => {
            console.error("Error deleting student:", error);
        });
}
