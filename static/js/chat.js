//get all of the parameters used to load the html, and includes the gd parameter
//loop through the url of the html, and break it up by '&', then breaks these values into key-value pairs
// and returns an object
getParameters = function(){
        var ret {};
        var queryString = window.location.search.substring(1);
        var params = queryString.split('&');

        <!--getting the parameters from the Url -->
        for(var co= 0; co < params.length; co++){
            var keyValue=params[co].split('=');
            ret[keyValue[0]]= unescape(keyValue[1]);
        }
        return ret;
    };

//gets called once everything on the page has been loaded
//then makes a call to the onApiReady event handlers
onClientReady = function(){
        gapi.hangout.onApiReady.add(function(e){
            //check to make sure the api is ready, if it call  onApiReady()
            if(e.isApiReady){
                onApiReady();
            }
        });
    };

//
onApiReady= function(){
    var param = getParameters();
    var now = new Date();
    //gets the hangout url that we are currently in
    var hangoutURL = gapi.hangout.getHangoutUrl();
    var callbackUrl = 'register _hangout.json';

    //Jquery ajax function call
    //Sets up a call using Json. Sends the values as part of a parameter list and get Json structure
    $.ajax({
    url:callbackUrl,
    dataType:'json',
    //parameters
    data:{
    "hangoutUrl":hangoutUrl,
    "topic":param["gd"]
    }
    }).done(function(data,status,xhr){

//set the message on the screen to whatever we get from Json
    $('#msg').html(data.msg);
    }).fail(function(xhr,stats,error)){
    $("#msg").html("There was a problem contacting the help service .Please try again. ("*textStatus+")  ")
    })



    })
}