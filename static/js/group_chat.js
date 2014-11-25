// Gobal variable for lms299.groupchat so that all subsequent functions
// can be registered under this namespace.
var lms299 = {
  groupchat: {
    // Adds a callback that will be called when the Google+ Hangout app is finished loading.
    onClientReady: function() {
      gapi.hangout.onApiReady.add(
        function(eventObj) {
        sendHangoutsUrl();

        gapi.hangout.av.onCameraMute.add(function(e) {
          updateUserSettingCamera(e.isCameraMute);
        });

        gapi.hangout.av.onMicrophoneMute.add(function(e) {
          updateUserSettingMicrophone(e.isMicrophoneMute);
        });
      });

      // Retrieves the request parameter value for passed in parameter name.
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
      
      // Sends the Hangouts URL to the lms299 web2py instance via an AJAX call.
      function sendHangoutsUrl() {
        $.ajax({
          contentType: 'application/json',
          type: 'POST',
          url: "http://127.0.0.1:8000/lms299/groupchat/hangouts_url_for_session.json",
          data: '{ "sessionId": "1", "hangoutsUrl": "' + gapi.hangout.getHangoutUrl() + '"}',
          dataType: 'json'
        });
      }

      // Sends the updated camera status to the lms299 web2py instance  via an AJAX call.
      function updateUserSettingCamera(muteCamera) {
        $.ajax({
          contentType: 'application/json',
          type: 'POST',
          url: "http://127.0.0.1:8000/lms299/groupchat/update_user_settings_camera.json",
          data: '{ "muteCamera": "' + muteCamera + '"}',
          dataType: 'json'
        });
      }

      // Sends the updated microphone status to the lms299 web2py instance  via an AJAX call.
      function updateUserSettingMicrophone(muteMicrophone) {
        $.ajax({
          contentType: 'application/json',
          type: 'POST',
          url: "http://127.0.0.1:8000/lms299/groupchat/update_user_settings_microphone.json",
          data: '{ "muteMicrophone": "' + muteMicrophone + '"}',
          dataType: 'json'
        });
      }

      // Updates the Google+ Hanougts instance settings using the passed in parameters.
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
