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


// Filtreleme işlemi
function applyFilters() {
    const numberMin = parseInt(document.getElementById("numberMin").value) || 0;
    const numberMax = parseInt(document.getElementById("numberMax").value) || Infinity;
    const firstLetter = document.getElementById("firstLetterFilter").value;
    const searchQuery = document.getElementById("searchInput").value.toUpperCase();

    fetch("/api/students")
        .then(response => response.json())
        .then(data => {
            const filteredStudents = data.filter(student => {
                const num = parseInt(student.student_number);
                const firstName = student.first_name.toUpperCase();

                let visible = true;

                if (num < numberMin || num > numberMax) visible = false;
                if (firstLetter && !firstName.startsWith(firstLetter)) visible = false;
                if (searchQuery && !firstName.includes(searchQuery)) visible = false;

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
