// const recordAudio = () =>
//   new Promise(async resolve => {
//     const stream =await navigator.mediaDevices.getUserMedia({ audio: true });
//       const mediaRecorder = new MediaRecorder(stream);
//       mediaRecorder.mimeType = "audio/wav";
//       const audioChunks = [];
//
//       mediaRecorder.addEventListener("dataavailable", event => {
//         audioChunks.push(event.data);
//     });
//
//     const start = () => mediaRecorder.start();
//
//     const stop = () =>
//       new Promise(resolve => {
//         mediaRecorder.addEventListener("stop", () => {
//           const audioBlob = new Blob(audioChunks);
//           const audioUrl = URL.createObjectURL(audioBlob);
//           const audio = new Audio(audioUrl);
//           const source  = audio.src;
//           const play = () => audio.play();
//           resolve({ audioBlob, audioUrl, play });
// 					console.log(audioBlob);
// 					$.ajax({
// 				    type: 'POST',
// 				    url: '/send',
// 				    data: audioBlob,
// 				    processData: false,
// 				    contentType: false,
// 				    success: function(response) {
// 				        alert(response);
// 				    }
// 					});
//         });
//         mediaRecorder.stop();
//       });
//
//     resolve({ start, stop });
//   });
//
// function doStuff(){
// 	const sleep = time => new Promise(resolve => setTimeout(resolve, time));
// (async () => {
//   const recorder = await recordAudio();
//   recorder.start();
//   await sleep(3000);
//   const audio = await recorder.stop();
//   audio.play();
// })();
// }
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
		        alert(response);
		    }
			});
}
function doStuff(){
	recognition.start();
}
