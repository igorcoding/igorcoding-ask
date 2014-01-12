var firstFetch = true;

$(document).ready(function () {
    google.load("visualization", "1", {packages:["corechart"], callback : ajaxTagChart});
});

function ajaxTagChart() {
    var targetUrl = "http://localhost/chart_data";
    var chart = new google.visualization.BarChart(document.getElementById('tag_chart'));
    $.ajax({
              type: "GET",
              url: targetUrl
            })
              .done(function(data) {
                    if (firstFetch || data['new'])
                        drawChart(chart, data);
                    firstFetch = false;
                    setTimeout(ajaxTagChart, 3000);
              })
              .fail(function(msg) {
                    console.log("could not fetch data");
                    setTimeout(ajaxTagChart, 3000);
              });
}

function drawChart(chart, chartData) {
    function colorizeRand(dataTable, row) {
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

    function colorize(dataTable, row) {
        var max = 0;
        for (var i = 0; i < dataTable.getNumberOfRows(); ++i) {
            var value = dataTable.getValue(i, 1);
            if (value > max)
                max = value;
        }

        var lowMax = max / 3;
        var midMax = 2 * max / 3;
        var highMax = max;

        var currentValue = dataTable.getValue(row, 1);
        if (currentValue <= lowMax)
            return "#21C273";
        if (currentValue <= midMax)
            return "#E0DC53";
        return "#D4413A";
    }

    function colorizer() {
        var $colorizer = $('input[name="ColorizeMethod"]:checked');
        var value = $colorizer.attr("value");
        if (value == "Wise")
            return colorize;
        else
            return colorizeRand;
    }

    if (chartData != null)
    {
        var rawData = chartData['data'];
        var data = new google.visualization.DataTable();

        data.addColumn('string', rawData['cols'][0]);
        data.addColumn('number', rawData['cols'][1]);

        var rows = rawData.rows;
        for (var i = 0; i < rows.length; ++i) {
            data.addRow([rows[i].tag, rows[i].count]);
        }

        var view = new google.visualization.DataView(data);
        view.setColumns([0, 1,
                        { calc: "stringify",
                          sourceColumn: 1,
                          type: "string",
                          role: "annotation" },
                        { calc: colorizer(),
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