document.addEventListener("DOMContentLoaded", () => {
    fetchInstructors();

    document.getElementById("searchInput").addEventListener("input", applyFilters);
    document.getElementById("minId").addEventListener("input", applyFilters);
    document.getElementById("maxId").addEventListener("input", applyFilters);
    document.getElementById("titleFilter").addEventListener("change", applyFilters);
});

let allInstructors = [];

function fetchInstructors() {
    fetch("/api/instructors")
        .then(response => response.json())
        .then(data => {
            allInstructors = data;
            renderTable(allInstructors);
        })
        .catch(error => console.error("Error fetching instructors:", error));
}

function renderTable(instructors) {
    const tbody = document.getElementById("instructorTableBody");
    tbody.innerHTML = "";

    instructors.forEach(instructor => {
    const row = `
        <tr>
            <td>${instructor.id}</td>
            <td>${instructor.name}</td>
            <td>${instructor.title}</td>
            <td>${instructor.email}</td>
            <td>
                <a href="/instructors/edit/${instructor.id}" class="btn btn-sm btn-primary">Edit</a>
                <button class="btn btn-danger btn-sm" onclick="deleteInstructor(${instructor.id})">Delete</button>
                <button class="btn btn-primary btn-sm" onclick="location.href='/students/charts?student_id={{ ${student.id }}'">Charts</button>
            </td>
        </tr>
    `;
    tbody.innerHTML += row;
});

    
}

function applyFilters() {
    const search = document.getElementById("searchInput").value.toLowerCase();
    const minId = document.getElementById("minId").value.trim();
    const maxId = document.getElementById("maxId").value.trim();
    const titleFilter = document.getElementById("titleFilter").value;

    const filtered = allInstructors.filter(instructor => {
        const matchesName = instructor.name.toLowerCase().includes(search);
        const matchesTitle = titleFilter === "" || instructor.title === titleFilter;
        const id = parseInt(instructor.instructor_id);
        const matchesMin = minId === "" || id >= parseInt(minId);
        const matchesMax = maxId === "" || id <= parseInt(maxId);

        return matchesName && matchesTitle && matchesMin && matchesMax;
    });

    renderTable(filtered);
}

function deleteInstructor(id) {
    if (!confirm("Are you sure you want to delete this instructor?")) return;

    fetch(`/api/instructors/${id}`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            alert("Instructor deleted successfully.");
            window.location.reload();
        } else {
            alert("Failed to delete instructor.");
        }
    })
    .catch(error => console.error("Error deleting instructor:", error));
}