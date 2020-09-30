var ctx = document.getElementById("score-transition");

var myLineChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [
        "Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.",
        "Sep.", "Oct.", "Nov.", "Dec."
    ],
    datasets: [
      {
        label: "課題発見力",
        data: data, //[35, 35, 40, 46, 52, 54, 60, 70, 70, 70, 70, 71],
        borderColor: "salmon",
        backgroundColor: "rgba(0,0,0,0)",
      },
    ],
  },
  options: {
    title: {
      display: false,
    },
    scales: {
      yAxes: [
        {
          ticks: {
            suggestedMax: 80,
            suggestedMin: 0,
            stepSize: 10,
            callback: function (value, index, values) {
              return value;
            },
          },
        },
      ],
    },
  },
});