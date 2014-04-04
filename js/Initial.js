var count=1;

function initialize() {
  var mapOptions = {
    center: new google.maps.LatLng(22.418765,114.208242),
    zoom: 13
  };
  var map = new google.maps.Map(document.getElementById('map-canvas'),
    mapOptions);
  
  var marker = new google.maps.Marker({
    map: map,
    position: new google.maps.LatLng(22.413533,114.21031),
    draggable: true
  });

  var input = /** @type {HTMLInputElement} */(
      document.getElementById('pac-input'));

  var types = document.getElementById('type-selector');
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  var autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.bindTo('bounds', map);
  autocomplete.setTypes([]);

  var infowindow = new google.maps.InfoWindow();
  var marker = new google.maps.Marker({
    map: map,
    anchorPoint: new google.maps.Point(0, -29)
  });

  google.maps.event.addListener(autocomplete, 'place_changed', function() {
    infowindow.close();
    marker.setVisible(false);
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      return;
    }

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);  // Why 17? Because it looks good.
    }
    marker.setPosition(place.geometry.location);
    marker.setVisible(true);
    coordinate=place.geometry.location;

    var address = '';
    if (place.address_components) {
      address = [
        (place.address_components[0] && place.address_components[0].short_name || ''),
        (place.address_components[1] && place.address_components[1].short_name || ''),
        (place.address_components[2] && place.address_components[2].short_name || '')
      ].join(' ');
    }

    infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
    infowindow.open(map, marker);
  });
}

google.maps.event.addDomListener(window, 'load', initialize);

var n;
var min=0;
var flag=0;

function deleteTime(divNum) {
	event.preventDefault();
	$('#'+divNum).remove();
	min++;
	if(flag<4)
  		$("#confirm_date").removeAttr('disabled');
}

function setTime() {
	event.preventDefault();
	var content=$('#selector').val();
	var divIdName;
 	divIdName="my"+count+"Div";  
 	
  	$('#timeContent').append(' <div id='+divIdName+'>'+content+'<a href="#" onclick="deleteTime(\'' + divIdName + '\')">   Delete</a></div>');
  	count++;
  	var flag=count-min;
  	if(flag==4)
  		$("#confirm_date").attr("disabled", "disabled");
  	
}

function submitComment(){
	event.preventDefault();
	var comment=$('#commentContent').val();
	$('#commentTable').append('<tr><td>'+comment+'</td><td>WANG WEI</td></tr>');
	$('#commentTable tr:last').after('<tr></tr>');
}

function submitForm(){
  if($('#input-loc')===''){
        alert("location cannot be null!");
    }
    else
    {
       $.ajax({url:'/event/submit',
    type:'POST',
    data: {name:$("#input-name").val(), my1Time:$("#my1Div").val(), my2Time:$("#my2Div").val(), my3Time:$("#my3Div").val(), location:$("#input-loc").val(), coordinate:coordinate}  // simulated server delay
}).done(function (bal) {
    alert(bal);
}).fail(function (jqXHR, textStatus) {
    alert("Request failed: " + textStatus);
});
    }
}


$( document ).ready(function() {

	var now = new Date();
	var day = ("0" + now.getDate()).slice(-2);
	var month = ("0" + (now.getMonth() + 1)).slice(-2);
	var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
	$('#selector').val(today);
	
});
