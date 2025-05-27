document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("editCourseForm");
  const instructorSelect = document.getElementById("instructor");
  const pathParts = window.location.pathname.split('/');
  const courseId = pathParts[pathParts.length - 1];

  // 1. Öğretmenleri çek ve select'e doldur
  fetch("/api/instructors")
    .then(response => response.json())
    .then(instructors => {
      instructors.forEach(i => {
        const option = document.createElement("option");
        option.value = i.id;
        option.textContent = i.name;
        instructorSelect.appendChild(option);
      });

      // 2. Kursu çek ve formu doldur
      return fetch(`/api/courses/${courseId}`);
    })
    .then(response => response.json())
    .then(course => {
      document.getElementById("courseName").value = course.name;
      document.getElementById("courseCode").value = course.code;
      document.getElementById("courseCredit").value = course.credit;
      instructorSelect.value = course.instructor_id; // id üzerinden eşleştir
    })
    .catch(error => {
      console.error("Error loading data:", error);
      alert("Failed to load course or instructors.");
    });

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const updatedCourse = {
      name: document.getElementById("courseName").value.trim(),
      code: document.getElementById("courseCode").value.trim(),
      credit: parseInt(document.getElementById("courseCredit").value),
      instructor_id: parseInt(document.getElementById("instructor").value)
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
