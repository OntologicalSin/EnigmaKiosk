try {
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
}
catch(e) {
  console.error(e);
  $('.no-browser-support').show();
  $('.app').hide();
}
recognition.onstart = function() {
  console.log('Voice recognition activated. Try speaking into the microphone.');
}

recognition.onspeechend = function() {
  console.log('You were quiet for a while so voice recognition turned itself off.');
}

recognition.onerror = function(event) {
  if(event.error == 'no-speech') {
    console.log('No speech was detected. Try again.');
  };
}
recognition.onresult = function(event) {

  var current = event.resultIndex;
  var transcript = event.results[current][0].transcript;
  console.log(transcript);
	$.ajax({
		    type: 'POST',
		    url: '/send',
		    data: transcript,
		    processData: false,
		    contentType: false,
		    success: function(response) {
		        window.location.reload();
		    }
			});
}

function doStuff(){
	recognition.start();
}

function sayStuff(){
    var audio = new Audio('loud.mp3');
    audio.loop = false;
    audio.play();
}

function deleteStuff(){
  $.ajax({
		    type: 'POST',
		    url: '/reset',
		    data: null,
		    processData: false,
		    contentType: false,
		    success: function(response) {
		        window.location.reload(true);
		    }
			});

}
