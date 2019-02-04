"use strict"

var socket = io.connect('http://' + document.domain + ':' + location.port);

var listmembers = []

socket.on('connect', function() {

  console.log(socket)

  var myDiv = document.createElement('div');
  myDiv.innerHTML = "my id is : " + socket.id;
  document.body.append(myDiv);
  socket.emit('my event', {data: 'I\'m connected!'});

});

socket.on('send_list_members', function(data) {
  listmembers = data;

  let dataselect = document.getElementById("mySelect");
  listmembers.data.forEach(element => {

  var option = document.createElement("option");
  if(element==socket.id){
    option.text = "me";
  }
  else{
    option.text = element;
  }
  dataselect.add(option);
  
  
  
});
  
});

socket.emit('message','Hello my chat server!!');


socket.on('follow_message', function(data){

  console.log("message followed:")
  console.log(data)
  var now = new Date();
  var isoString = now.toISOString();
  var textfollowed = '<br />' + "[" + data['sender'] + "] at " + isoString + ": " + data['message'];
  document.getElementById("receivedmessages").innerHTML += textfollowed;
});

function sendmessage() {
  var messagetosend = document.getElementById("messagetext").value;
  
  var selectdata = document.getElementById("mySelect");
  var receiver = selectdata.options[selectdata.selectedIndex].text;
  socket.emit('chatmessage',{'receiver': receiver, 'messagetosend': messagetosend})
//  console.log("my data is : ");
//    socket.emit('message',alert(dataform.elements.message.value))
//  console.log(dataform.elements.message)
}
