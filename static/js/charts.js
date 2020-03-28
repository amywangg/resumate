$(document).ready(function () {
    GetAppData();
    GetSkillData();
});

var GetAppData = function () {
    var applicants = []
    var matches = []
    var titles = []
    $.ajax({
        url: '/jobapplicants',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            $.each(data, function (k, v) {
                applicants.push(v.Applicants)
                matches.push(v.Matches)
                titles.push(v.Job_Title)
            });
            var barChartData = {
                labels: titles,
                datasets: [{
                    label: 'Applicants',
                    backgroundColor: 'rgb(38, 222, 151,0.5)',
                    borderWidth: 3,
                    data: applicants
                }, {
                    label: 'Matches',
                    backgroundColor: 'rgb(252, 148, 3,0.5)',
                    borderWidth: 3,
                    data: matches
                }]
            };
            var ctx = document.getElementById('jobapplicants').getContext('2d');
            window.myBar = new Chart(ctx, {
                type: 'bar',
                data: barChartData,
                options: {
                    title: {
                        display: true,
                        text: 'Top Jobs: Applicants vs Matches',
                        fontSize: 14
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false
                    },
                    maintainAspectRatio: false,
                    responsive: true,
                    scales: {
                        xAxes: [{
                            stacked: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Job Title',
                                fontSize: 14
                            }
                        }],
                        yAxes: [{
                            stacked: true,
                            ticks: {
                                beginAtZero: true
                            },
                            scaleLabel: {
                                display: true,
                                labelString: '# of Applicants',
                                fontSize: 14
                            }
                        }]
                    }
                }
            });
        }
    });
};

var GetSkillData = function () {
    var skills = []
    var count = []
    $.ajax({
        url: '/topskills',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            var topskills = data.slice(0, 10)
            $.each(topskills, function (index, v) {
                skills.push(v[0])
                count.push(v[1])
            });
            console.log(count)
            var barChartData = {
                labels: skills,
                datasets: [{
                    label: '# of Hits',
                    backgroundColor: 'rgb(245, 66, 90, 0.5)',
                    borderWidth: 3,
                    data: count
                }]
            };
            var ctx = document.getElementById('skillstat').getContext('2d');
            window.myBar2 = new Chart(ctx, {
                type: 'bar',
                data: barChartData,
                options: {
                    title: {
                        display: true,
                        text: 'Top 10 Skills',
                        fontSize: 14
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false
                    },
                    maintainAspectRatio: false,
                    responsive: true,
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Skill',
                                fontSize: 14
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            },
                            scaleLabel: {
                                display: true,
                                labelString: '# of Hits',
                                fontSize: 14
                            }
                        }]
                    }
                }
            });
        }
    });
};
