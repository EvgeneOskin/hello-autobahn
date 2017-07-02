console.log("Runnning on AutobahnJS ", autobahn.version);

// the URL of the WAMP Router (Crossbar.io)
//
var wsuri;
if (document.location.origin == "file://") {
    wsuri = "ws://127.0.0.1:8080/ws";
} else {
    wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
        document.location.host + "/ws";
}

var user = {
    'authid': 'john',
    'ticket': 'some-random-string-for-the-user'
};

var onChallenge = function(session, method, extra) {
    if (method === 'ticket') {
        return user.ticket;
    } else {
        throw "Don't know how to challenge this method " + method;
    }
};

// the WAMP connection to the Router
var connection = new autobahn.Connection({
    url: wsuri,
    realm: "realm1",
    authmethods: ['ticket'],
    authid: user.authid,
    onchallenge: onChallenge
});


// timers
var t1, t2;

// fired when connection is established and session attached
connection.onopen = function (session, details) {
    console.log("Connected: ", session, details);

    var componentId = details.authid;
    var componentType = "JavaScript/Browser";

    console.log("Component ID is ", componentId);
    console.log("Component tpye is ", componentType);

    // CALL a remote procedure every 2 seconds .. forever
    var x = 0;

    t2 = setInterval(function () {

        session.call('com.eoskin.hello', ['Mike']).then(
            function (res) {
                var result = res[0];
                var id = res[1];
                var type = res[2];
                console.log("-----------------------");
                console.log("hello result:", result);
                console.log("from component " + id + " (" + type + ")");

            },
            function (err) {
                console.log("-----------------------");
                console.log("add2() error:", err);
            }
        );

    }, 2000);
};

// fired when connection was lost (or could not be established)
connection.onclose = function (reason, details) {
    console.log("Connection lost: " + reason);
    console.log(details);

    clearInterval(t1);
    t1 = null;

    clearInterval(t2);
    t2 = null;
}


// now actually open the connection
connection.open();
