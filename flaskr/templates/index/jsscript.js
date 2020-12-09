var request = new XMLHttpRequest();
request.open('POST', '/searching')
request.onload = function(){
if (request.status ===200 && request.responseText ==='done')
  {window.location = '/changed';}
  else {
  alert('Something went wrong');}
};

request.onerror = function() {
alert('Something went wrong');
}:
request.send();