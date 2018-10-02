var gKey = gKeyTemp;
$("#jsdelz").remove();
console.log(gKey);

var map;
function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
	  center: {lat: -34.397, lng: 150.644},
	  zoom: 8
	});
}

function send() {
   console.log($('.textbox').val());
   var search_word = $('.textbox').val();
   var qurl="http://localhost:5000";
   $.ajax({
            type: "POST",
            cache: false,
            data:{keyword:search_word},
            url: qurl,
            dataType: "json",
            success: function(data) { 
                $('body').append(data);                    
            },
            error: function(jqXHR) {
                alert("error: " + jqXHR.status);
                console.log(jqXHR);
            }
        })
};