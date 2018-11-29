
new Chart(document.getElementById("doughnut-chart"), {
    type: 'doughnut',
    data: {
      labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: [2478,5267,734,784,433]
        }
      ]
    },
    options: {
      responsive: false,
      title: {
        display: true,
        text: 'Distribution of Assets in your Portfolio'
      },
      legend: {
          display: true,
          labels: {
            fontSize: 8,
            boxWidth: 20
          }
      }
    }
});