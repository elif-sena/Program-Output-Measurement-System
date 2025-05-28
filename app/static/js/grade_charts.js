window.addEventListener('DOMContentLoaded', () => {
    // Course averages chart data
    const courseLabels = Object.keys(courseAvgData);
    const courseGrades = Object.values(courseAvgData);

    const ctxCourse = document.getElementById('courseAvgChart').getContext('2d');
    new Chart(ctxCourse, {
        type: 'bar',
        data: {
            labels: courseLabels,
            datasets: [{
                label: 'Course Grades',
                data: courseGrades,
                backgroundColor: 'rgba(54, 162, 235, 0.6)'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // Program Outcome averages chart data
    const poLabels = poAvgData.map(po => po.code);
    const poGrades = poAvgData.map(po => po.average);

    const ctxPO = document.getElementById('poAvgChart').getContext('2d');
    new Chart(ctxPO, {
        type: 'bar',
        data: {
            labels: poLabels,
            datasets: [{
                label: 'PO Averages',
                data: poGrades,
                backgroundColor: 'rgba(255, 99, 132, 0.6)'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
});
