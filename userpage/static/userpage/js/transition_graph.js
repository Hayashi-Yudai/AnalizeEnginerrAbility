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
                label: "サーチ力",
                data: star_scores,
                borderColor: "#329ad1",
                backgroundColor: "rgba(50, 154, 209, 0.1)",
                /*
                backgroundColor: "rgba(0,0,0,0)",
                 */
            },
            {
                label: "課題発見力",
                data: issue_scores,
                borderColor: "#cd5c5c",
                backgroundColor: "rgba(205, 92, 92, 0.1)",
            },
            {
                label: "課題解決力",
                data: pull_request_scores,
                borderColor: "#00a497",
                backgroundColor: "rgba(0, 164, 151, 0.1)"
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