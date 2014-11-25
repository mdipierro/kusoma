var lms299 = {
  groupchat: {
    onClientReady: function() {
      gapi.hangout.onApiReady.add(
        function(eventObj) {
        sendHangoutsUrl();
      });
      
      function getParameter(name) {
        var pageUrl = window.location.search.substring(1);
        var urlParams = pageUrl.split('&');
        
        for (var i = 0; i < urlParams.length; i++) {
          var param = urlParams[i].split('=');
          if (param[0] == name) {
            alert (param[1]);
          }
        }
      }
      
      function sendHangoutsUrl() {
        $.ajax({
          contentType: 'application/json',
          type: 'POST',
          url: "http://127.0.0.1:8000/lms299/groupchat/hangouts_url_for_session.json",
          data: '{ "sessionId": "1", "hangoutsUrl": "' + gapi.hangout.getHangoutUrl() + '"}',
          dataType: 'json'
        });
      }
        
      function setUserChatSettings(muteCamera, muteMicrophone) {
        gapi.hangout.av.setCameraMute(muteCamera);
        gapi.hangout.av.setMicrophoneMute(muteMicrophone);
      }
    }
  }
}

$(document).ready(function () {
  lms299.groupchat.onClientReady();
});
