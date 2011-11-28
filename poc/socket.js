window.onload = function(){
    var socket = new MozWebSocket("ws://localhost:9000/");
    socket.onmessage = function(e) {
	console.log(e.data);
    };

};