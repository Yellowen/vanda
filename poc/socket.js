function make_socket(address){
    var Socket = null;
    if (typeof WebSocket == 'function'){
	Socket = WebSocket;
    }
    if (typeof MozWebSocket == 'function'){
	Socket = MozWebSocket;
    }
    var socket = new Socket(address);
    return socket;
}
window.onload = function(){
    socket = make_socket("ws://localhost:9000/");
    socket.onmessage = function(e) {
	console.log(e.data);
    };

};