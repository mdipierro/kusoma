$(document).ready(function() {
  console.log("ready!");
});

function sendMessage() {
  console.log("sendMessage()");
  gapi.hangout.data.sendMessage("Plz work!!!");
}

function showParticipants() {
  var participants = gapi.hangout.getParticipants();

  var retVal = '<p>Participants: </p><ul>';

  for (var index in participants) {
    var participant = participants[index];

    if (!participant.person) {
      retVal += '<li>A participant not running this app</li>';
    }
    retVal += '<li>' + participant.person.displayName + '</li>';
  }

  retVal += '</ul>';

  var div = document.getElementById('participantsDiv');

  div.innerHTML = retVal;
}

function onClientReady() {
  // When API is ready...                                                         
  gapi.hangout.onApiReady.add(
      function(eventObj) {
        document.getElementById('showParticipants')
          .style.visibility = 'visible';
        
        gapi.hangout.onParticipantsAdded.add(function(e) {
          console.log(e);
        });
        
        gapi.hangout.data.onMessageReceived.add(function(e) {
          console.log("onMessageReceived()");
          $('#msg').html("test: " + e);
        });
        
        $.ajax({
          contentType: 'application/json',
          type: 'POST',
          url: "http://127.0.0.1:8000/lms299/groupchat/hagouts_url_for_session.json",
          data: '{ "name": "Test", "location": "Chicago" }',
          dataType: 'json'
        })

        var pageUrl = window.location.search.substring(1);
        var urlParams = pageUrl.split('&');
        console.log(urlParams);
        for (var i = 0; i < urlParams.length; i++) {
          var param = urlParams[i].split('=');
          if (param[0] == 'gd') {
            alert (param[1]);
          }
        }
      });
}