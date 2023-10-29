alert('test');

const usageBigBall = document.getElementById('myChart');

new Chart(usageBigBall, {
    type: 'bar',
    data: {
    labels: labels[0],
    datasets: [{
        label: 'Bolas Grandes',
        data: labels[1][0],
        borderWidth: 1,
    },
    {
        label: 'Bolas Pequenas',
        data: labels[1][1],
        borderWidth: 0.5
    }
]
    },
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    },
    responsive: true
    }
});