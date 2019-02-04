"use strict"

var socket = io.connect('http://' + document.domain + ':' + location.port);


/*
When the user connect to the server, he get an id
*/
socket.on('connect', function() {
  var myDiv = document.createElement('div');
  myDiv.innerHTML = "my id : " + socket.id;
  var form = document.getElementById("myForm");
  form.parentNode.insertBefore(myDiv, form);
});

/*
When the server send the list of all clients, the user take the list and put
it into the select element of the form
*/

socket.on('send_list_members', function(data) {
  var listmembers = data;

  var myForm = document.getElementById("myForm");

  var dataselect = document.getElementById("mySelect");
  if(dataselect === null) {
    dataselect = document.createElement("select");
    dataselect.id = "mySelect";
    myForm.appendChild(dataselect);
  }
  
  dataselect.innerHTML = null
  
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

/*
When the user receive a message from the server, he print the name of the
initial sender and the content of the message, with the actual date
*/

socket.on('follow_message', function(data){
  var now = new Date();
  var isoString = now.toISOString();
  var textfollowed = '<br />' + "[" + data['sender'] + "] at " + isoString + ": " + data['message'];
  document.getElementById("receivedmessages").innerHTML += textfollowed;
});

/*
The function to send a message to the server
*/

function sendmessage() {
  var messagetosend = document.getElementById("messagetext").value;
  
  var selectdata = document.getElementById("mySelect");
  var receiver = selectdata.options[selectdata.selectedIndex].text;
  socket.emit('chatmessage',{'receiver': receiver, 'messagetosend': messagetosend})
}
