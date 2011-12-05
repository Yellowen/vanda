var io = require('socket.io').listen(9000);

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
