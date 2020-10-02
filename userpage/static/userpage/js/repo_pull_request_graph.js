var ctx_repo_pr = document.getElementById("repo-pull-request");

var myLineChart = new Chart(ctx_repo_pr, {
    type: "bar",
    data: {
        labels: [
            "Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.",
            "Sep.", "Oct.", "Nov.", "Dec."
        ],
        datasets: [
            {
                label: "Your PRs",
                data: [1, 2, 3, 1, 3, 0, 3, 1, 9, 3],
                borderColor: "rgba(0, 0, 0, 0)",
                backgroundColor: "rgba(255, 0, 0, 0.5)",
            },
            {
                label: "Others' PRs",
                data: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
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
                        stepSize: 2,
                        callback: function (value, index, values) {
                            return value;
                        },
                    },
                },
            ],
        },
    },
});
