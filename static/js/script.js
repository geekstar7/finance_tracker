document.addEventListener('DOMContentLoaded', () => {
  fetch('/data')
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById('expenseChart').getContext('2d');
      const labels = data.map(row => row[0]);
      const values = data.map(row => row[1]);

      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            label: 'Expenses by Category',
            data: values,
            backgroundColor: [
              '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
            ]
          }]
        },
        options: {
          responsive: true
        }
      });
    });
});