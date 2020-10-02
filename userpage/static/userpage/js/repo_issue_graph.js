var ctx_repo_issue = document.getElementById("repo-issue");

var myLineChart = new Chart(ctx_repo_issue, {
    type: "bar",
    data: {
        labels: [
            "Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.",
            "Sep.", "Oct.", "Nov.", "Dec."
        ],
        datasets: [
            {
                label: "Your Issues",
                data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                borderColor: "rgba(0, 0, 0, 0)",
                backgroundColor: "rgba(255, 0, 0, 0.5)",
            },
            {
                label: "Others' Issues",
                data: [7, 5, 6, 8, 7, 7, 12, 6, 10, 11],
                borderColor: "rgba(0, 0, 0, 0)",
                backgroundColor: "rgba(198, 198, 198, 0.5)",
            },
        ],
    },
    options: {
        title: {
            display: false,
        },
        scales: {
            xAxes: [{
                stacked: true,
            }],
            yAxes: [
                {
                    stacked: true,
                    ticks: {
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
