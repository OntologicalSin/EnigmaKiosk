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
		    data: res.from.language.iso,
		    processData: false,
		    contentType: false,
		    success: function(response) {
		        window.location.reload();
		    }
			});
}

// Enter an API key from the Google API Console:
//   https://console.developers.google.com/apis/credentials
const apiKey = "AIzaSyCJ7_NoaZ4cFjupJuTikKc0-Oq1wH1sAdg";

// Set endpoints
const endpoints = {
  translate: "",
  detect: "detect",
  languages: "languages"
};

// Abstract API request function
function makeApiRequest(endpoint, data, type, authNeeded) {
  url = "https://www.googleapis.com/language/translate/v2/" + endpoint;
  url += "?key=" + apiKey;

  // If not listing languages, send text to translate
  if (endpoint !== endpoints.languages) {
    url += "&q=" + encodeURI(data.textToTranslate);
  }

  // If translating, send target and source languages
  if (endpoint === endpoints.translate) {
    url += "&target=" + data.targetLang;
    url += "&source=" + data.sourceLang;
  }

  // Return response from API
  return $.ajax({
    url: url,
    type: type || "GET",
    data: data ? JSON.stringify(data) : "",
    dataType: "json",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json"
    }
  });
}

// Translate
function translate(data) {
  makeApiRequest(endpoints.translate, data, "GET", false).success(function(
    resp
  ) {
    $(".target").text(resp.data.translations[0].translatedText);
    $("h2.detection-heading").hide();
    $("h2.translation-heading, p").show();
  });
}

// Detect language
function detect(data) {
  makeApiRequest(endpoints.detect, data, "GET", false).success(function(resp) {
    source = resp.data.detections[0][0].language;
    conf = resp.data.detections[0][0].confidence.toFixed(2) * 100;

    $(".source-lang option")
      .filter(function() {
        return $(this).val() === source; //To select Blue
      })
      .prop("selected", true);
    $.when(getLanguageNames()).then(function(data) {
      $("p.target").text(data[source] + " with " + conf + "% confidence");
    });
    $("h2.translation-heading").hide();
    $("h2.detection-heading, p").show();
  });
}

// Get languages
function getLanguages() {
  makeApiRequest(endpoints.languages, null, "GET", false).success(function(
    resp
  ) {
    $.when(getLanguageNames()).then(function(data) {
      $.each(resp.data.languages, function(i, obj) {
        $(".source-lang, .target-lang").append(
          '<option value="' +
            obj.language +
            '">' +
            data[obj.language] +
            "</option>"
        );
      });
    });
  });
}

function getLanguageNames() {
  return $.getJSON("https://api.myjson.com/bins/155kj1");
}

// On document ready
$(function() {
  window.makeApiRequest = makeApiRequest;
  var translationObj = {};

  // Popuplate source and target language dropdowns
  getLanguages();

  $(document)
    // Bind translate function to translate button
    .on("click", "button.translate", function() {
      translationObj = {
        sourceLang: $(".source-lang").val(),
        targetLang: $(".target-lang").val(),
        textToTranslate: transcript
      };

      if (translationObj.targetLang !== null) {
        translate(translationObj);
      } else {
        alert("Please select a target language");
      }
    })
    // Bind detect function to detect button
    .on("click", "button.detect", function() {
      translationObj = {
        textToTranslate: transcript
      };

      detect(translationObj);
    });
});


function doStuff(lang){

	recognition.start();
  recognition.lang = lang;
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
