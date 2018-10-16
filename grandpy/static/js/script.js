var nb = 0;
var words = ["petit","bichon","ptit loup","grand"];

$('body').keydown (function(e){
	if(e.which == 13){
		send();
	}
});

  function send() {
    var search_word = $('.textbox').val();
    if(search_word != ""){
      $('.textbox').val("");
      var qurl=window.location.href;
      // Create the question renderer
      var loading = document.createElement("div");
      loading.className = "loader";
      var container = document.createElement("div");
      container.className = "col-lg-12 col-offset-3";
      var questionRow = document.createElement("div");
      questionRow.className = "row";
      container.append(questionRow);
      var questionPad = document.createElement("div");
      questionPad.className = "col-lg-7";
      questionRow.append(questionPad);
      var questionBox = document.createElement("div");
      questionBox.className = "col-lg-5 text-right question";
      questionBox.append(search_word);
      questionRow.append(questionBox);
      $('#chat').append(container,loading);
      var objDiv = document.getElementById("chat");
      objDiv.scrollTop = objDiv.scrollHeight;
      $.ajax({
              type: "POST",
              cache: false,
              data:{keyword:search_word},
              url: qurl,
              dataType: "json",
              success: function(data) { 
                  var resp = data;
                  if(resp != "error" && resp != "AccessDenied" && resp != null && resp != "InternalError"){
                      console.log(resp);
                      // Create the answer renderer
                      var ansRow = document.createElement("div");
                      ansRow.className = "row";
                      var preText = ""
                      var ansTxtDesc = document.createElement("div");
                      ansTxtDesc.className = "col-lg-7 grandpy-ans";
                      if(resp[1] != "NoTxt"){
                        if(search_word.includes("?")){
                          preText = "Bien sur mon "+ words[Math.floor(Math.random()*words.length)] + " ! Voici son addresse : ";
                        }
                        else{
                          preText = "Son addresse : ";
                        }
                        ansTxtDesc.append(preText + resp[0]['result']['formatted_address']); 
                      }
                      ansRow.append(ansTxtDesc);
                      var mapContainer = document.createElement("div");
                      mapContainer.className = "card narrower";
                      ansTxtDesc.append(mapContainer);
                      var mapBody = document.createElement("div");
                      mapBody.className = "card-body card-body-cascade text-center";
                      mapContainer.append(mapBody);
                      var map;
                      var mapelem = document.createElement("div");
                      mapelem.setAttribute('id','map'+nb);
                      mapelem.className = "z-depth-1 map";                  
                      mapBody.append(mapelem);
                      var ansTxt = document.createElement("div");
                      ansTxt.className = "col-lg-7 grandpy-ans";
                      if(resp[1] != "NoTxt"){
                        ansTxt.append(createText(resp));
                      }
                      else{
                        ansTxt.append("Je ne connais pas cet endroit malheureusement.");
                      }
                      ansRow.append(ansTxt);
                      container.append(ansRow);
                      objDiv.scrollTop = objDiv.scrollHeight;
                      loading.remove()
                      longlat = resp[0]['result']['geometry']['location'];
                      map = new google.maps.Map(mapelem, {
                        center: {lat: longlat['lat'], lng: longlat['lng']},
                        zoom: 8
                      });
                      var marker = new google.maps.Marker({
                      position: {lat: longlat['lat'], lng: longlat['lng']},
                        map: map,
                        title: resp[0]['result']['formatted_address']
                      });
                      map.setZoom(17);
                      map.panTo(marker.position);
                      objDiv.scrollTop = objDiv.scrollHeight;
                    }
                  else{
                    if(resp == "AccessDenied"){
                      var ansRow = document.createElement("div");
                      ansRow.className = "row";
                      var ansTxt = document.createElement("div");
                      ansTxt.className = "col-lg-7 grandpy-ans";
                      ansTxt.append("Il semblerais que mon accès a internet ne fonctionne plus !");
                      ansRow.append(ansTxt);
                      container.append(ansRow);
                      loading.remove()
                    }
                    else if(resp == "error" || resp == "InternalError"){
                      var ansRow = document.createElement("div");
                      ansRow.className = "row";
                      var ansTxt = document.createElement("div");
                      ansTxt.className = "col-lg-7 grandpy-ans";
                      ansTxt.append("Je n'ai pas très bien compris ce que vous m'avez dit !");
                      ansRow.append(ansTxt);
                      container.append(ansRow);
                      loading.remove()
                    }
                    else if(resp == null){
                      var ansRow = document.createElement("div");
                      ansRow.className = "row";
                      var ansTxt = document.createElement("div");
                      ansTxt.className = "col-lg-7 grandpy-ans";
                      ansTxt.append("Je n'ai pas très bien compris ce que vous m'avez dit !");
                      ansRow.append(ansTxt);
                      container.append(ansRow);
                      loading.remove()
                    }
                  }
                  nb += 1;                 
              },
              error: function(jqXHR) {
                  alert("error: " + jqXHR.status);
                  console.log(jqXHR);
              }
          })
  }
};

function createText(data){
  var articleUrl = data[1];
  var articleDesc = data[2];
  var txt = document.createElement('p');
  var url = document.createElement('a');
  var linkText = document.createTextNode("Wikipedia");
  if(articleUrl == null || articleDesc == "InternalError"){
    return "Oh je ne connais pas du tout cet endroit. Surement un trou de mémoire !"
  }
  else{
    if(articleDesc == ""){
      articleDesc = "Oh je ne connais pas grand-chose de cet endroit mais je peux te laisser aller sur Wikipedia pour avoir plus d'informations ! "
    }
    url.appendChild(linkText)
    url.href = articleUrl;
    url.setAttribute('target','_blank');
    txt.append(articleDesc + "[En savoir plus sur ") 
    txt.append(url);
    txt.append("]")
    return txt;
  }
}

