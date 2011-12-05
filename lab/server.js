var io = require('socket.io').listen(9000);
var net = require('net');

var unix = net.createServer(function(c) {
    console.log('Unix server connected');
    c.on('end', function() {
	console.log('Unix server disconnected');
    });
    
    c.on('data', function(data){
	console.log('[RECV]: ' + data);

    });
});

unix.listen("/tmp/websucks.sock", function() {
    console.log("unix listen");
});


io.configure(function () {
  io.set('transports', ['websocket']);
});

io.sockets.on('connection', function (socket) {
  socket.on('message', function (data) {
      console.log("A message received.");
      console.log(data);
  });
  socket.on('disconnect', function () {
      console.log("disconnected");
  });
});
