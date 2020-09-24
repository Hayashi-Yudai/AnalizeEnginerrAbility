var ctx = document.getElementById("score-transition");
var myLineChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul."],
    datasets: [
      {
        label: "スコア",
        data: [35, 35, 40, 52, 54, 60, 70],
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
            suggestedMax: 40,
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
