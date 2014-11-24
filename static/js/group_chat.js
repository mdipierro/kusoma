function onClientReady() {
  // When API is ready...                                                         
  gapi.hangout.onApiReady.add(
    function(eventObj) {
      sendHangoutsUrl();

      document.getElementById('showParticipants').style.visibility = 'visible';

      var pageUrl = window.location.search.substring(1);
      var urlParams = pageUrl.split('&');
      console.log(urlParams);
      for (var i = 0; i < urlParams.length; i++) {
        var param = urlParams[i].split('=');
        if (param[0] == 'gd') {
          alert (param[1]);
        }
      }

      function sendHangoutsUrl() {
        $.ajax({
          contentType: 'application/json',
          type: 'POST',
          url: "http://127.0.0.1:8000/lms299/groupchat/hagouts_url_for_session.json",
          data: '{ "sessionId": "1", "hangoutsUrl ": "' + gapi.hangout.getHangoutUrl() + '"}',
          dataType: 'json'
        });
      }
  });
}