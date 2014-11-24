
  {{
	  from gluon.serializers import json
  }}
  var jsonData = 
	  {{
		  response.write(json(message), escape=False)
	  }};

  if (jsonData == 'True')
  {
	$('#imgMessage').attr('src', '../static/images/note_message.png');
  }
