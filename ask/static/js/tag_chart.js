var newData = true;

google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(ajaxTagChart);

function ajaxTagChart() {
    var targetUrl = "http://localhost/chart_data";
    var chart = new google.visualization.ColumnChart(document.getElementById('tag_chart'));
    $.ajax({
              type: "GET",
              url: targetUrl
            })
              .done(function(data) {
                    if (data['new'])
                        newData = true;
                    if (newData || data['new'])
                        drawChart(chart, data);
                    newData = false;
                    setTimeout(ajaxTagChart, 3000);
              })
              .fail(function(msg) {
                    console.log("could not fetch data");
                    setTimeout(ajaxTagChart, 3000);
              });
}

function drawChart(chart, chartData) {
    function colorize(dataTable, row) {
        function get_random_color() {
            var letters = '0123456789ABCDEF'.split('');
            var color = '#';
            for (var i = 0; i < 6; i++ ) {
                color += letters[Math.round(Math.random() * 15)];
            }
            return color;
        }

        return get_random_color();
    }

    if (chartData != null)
    {
        var data = new google.visualization.DataTable(chartData['data']);

        var view = new google.visualization.DataView(data);
        view.setColumns([0, 1,
                        { calc: "stringify",
                          sourceColumn: 1,
                          type: "string",
                          role: "annotation" },
                        { calc: colorize,
                          type: "string",
                          role: "style"}]);

        var options = {
            title: chartData['title'],
            titleTextStyle: {fontSize: 18},
            hAxis: {title: chartData['hAxisTitle'], titleTextStyle: {color: 'black', italic: false}},
            legend: {position: 'none'}
        };
        chart.draw(view, options);
    }
    else
        console.log("could not fetch data");
}
/*
function drawChart323235246() {
    var chartData = getChartData();
    if (chartData != null)
    {
        var data = chartData['data'];
        var options = {
          title: chartData['title'],
          hAxis: {title: chartData['hAxisTitle'], titleTextStyle: {color: 'red'}}
        };

        if (chart == null)
            chart = new google.visualization.ColumnChart(document.getElementById('tag_chart'));
        chart.draw(data, options);
    }
    else
        console.log("could not fetch data");

    setTimeout(drawChart, 3000);
}
*/