function fetchProgressbar(targetUrl, cid) {
    $.ajax({
              type: "GET",
              url: targetUrl + cid
            })
              .done(function(msg) {
                    var data = JSON.parse(msg);
                    drawProgressBar(data["value"]);
                    fetchProgressbar(targetUrl, cid);
              })
              .fail(function(msg) {
                    console.log("could not fetch data");
                    setTimeout(fetchProgressbar(targetUrl, cid), 5000);
              });
}

function drawProgressBar(value) {
    var progressbar = $(".progress-bar");
    var current = parseInt(progressbar.attr("aria-valuenow"));
    var min = parseInt(progressbar.attr("aria-valuemin"));
    var max = parseInt(progressbar.attr("aria-valuemax"));


    progressbar.attr("aria-valuenow", value);
    $(".progress").find("span").text(value + "%");
    progressbar.css({"width": value + "%"});
}

jQuery(document).ready(function ($) {
    var targetUrl = "http://localhost/longpoll/listen/?cid=";
    var cid = "progressbar";
    console.log(targetUrl + cid);
    fetchProgressbar(targetUrl, cid);
});