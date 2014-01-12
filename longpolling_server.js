var http = require('http');
var url = require('url');
var querystring = require('querystring');

function getPath(request) {
    return url.parse(request.url);
}

function getGET(request) {
    return querystring.parse(getPath(request).query);
}

function getContentType(request) {
    if (typeof (request.headers['content-type']) === 'undefined')
        return "text/plain";
    return request.headers['content-type'];
}

var views = {
    requests: {},


    listen: function(request, response, GET, POST, originalPOST) {

        if (typeof (GET["cid"]) === "string") {
            if (typeof (views.requests[GET["cid"]]) === 'undefined') {
                views.requests[GET["cid"]] = [];
            }
            views.requests[GET["cid"]].push(response);

        }
        else {
            response.writeHead(200, {'Content-Type': 'text/plain'});
            response.write("No cid provided");
            response.end();
        }

    },

    publish: function(request, response, GET, POST, originalPOST) {

        response.writeHead(200, {'Content-Type': 'text/plain'});
        var cid = GET["cid"];
        if (typeof (cid) === "string") {
            if (typeof (views.requests[cid]) === 'undefined') {
                response.write("No listeners to this cid.\n");
                response.end();
            }
            else {
                if (POST == null) {
                    response.write("Expected POST request");
                }
                else {
                    var listenersLength = views.requests[cid].length;
                    for (var i = 0; i < listenersLength; ++i) {
                        var resp = views.requests[cid].pop();
                        resp.writeHead(200, {'Content-Type': getContentType(request)});
                        resp.write(originalPOST);
                        resp.end();
                    }
                    response.write("Success!");
                }

            }

            //response.write(views.requests);
        }
        else {
            response.write("No cid provided");
        }

        response.end();
    },

    notfound: function(request, response) {
        response.writeHead(404, {'Content-Type': 'text/plain'});
        response.write("Not found\n");
        response.end();
    }
};


function route(request, response, GET, POST, originalPOST) {
    var path = getPath(request);

    switch (path.pathname){
        case "/listen/":
            views.listen(request, response, GET, POST, originalPOST);
            break;
        case "/publish/":
            views.publish(request, response, GET, POST, originalPOST);
            break;
        default:
            views.notfound(request, response);
            return;
    }

}


function requestHandler(request, response) {
    request.setEncoding("utf8");

    if (request.method == "POST") {
        var postData = "";
        request.addListener("data", function(postDataChunk) {
            postData += postDataChunk;
        });

        request.addListener("end", function() {
            route(request, response, getGET(request), querystring.parse(postData), postData);
        });
    }
    else {
        route(request, response, getGET(request), null, null);
    }

}

http.createServer(requestHandler).listen(8888, "127.0.0.1");
console.log('Server running at http://127.0.0.1:8888/');