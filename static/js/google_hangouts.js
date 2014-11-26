$(document).ready(function () {
$( ".join-hangouts" ).submit(function( event ) {
  alert( "Handler for .submit() called." );
  event.preventDefault();
  event.submit();
});
});