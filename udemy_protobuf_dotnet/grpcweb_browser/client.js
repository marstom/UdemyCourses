const {RoomRegistrationRequest, ChatMessage} = require('./groom_pb.js');
const {GroomClient} = require('./groom_grpc_web_pb.js');

var client = new GroomClient(window.location.origin);

var request = new RoomRegistrationRequest();
request.setRoomName('rozne_tematey');
request.setUserName('Tomek');

client.registerToRoom(request, {}, (err, response) => {
  if (err) {
    console.error('gRPC-Web error:', err);
    // alert('Join failed: ' + err.message);
    return;
  }
  console.log(response.getJoined());
});

