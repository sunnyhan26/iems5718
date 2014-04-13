var count=1;
var coordinate='';
var time=["","",""];
var wrong=[0,0,0,0];

function initialize() {
  var mapOptions = {
    center: new google.maps.LatLng(22.413533,114.21031),
    zoom: 17
  };
 var map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
 var marker = new google.maps.Marker({
    map: map,
    position: new google.maps.LatLng(22.413533,114.21031),
    draggable: true
  });

  var input = /** @type {HTMLInputElement} */(document.getElementById('pac-input'));

  //var types = document.getElementById('type-selector');
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  //map.controls[google.maps.ControlPosition.TOP_LEFT].push(types);

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
    
    coordinate=place.geometry.location.lat()+','+place.geometry.location.lng();
    alert(coordinate);

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

  // Sets a listener on a radio button to change the filter type on Places
  // Autocomplete.
  /*function setupClickListener(id, types) {//
    var radioButton = document.getElementById(id);
    google.maps.event.addDomListener(radioButton, 'click', function() {
      autocomplete.setTypes(types);
    });*/
   
  }
 //google.maps.event.addDomListener(window, 'load', initialize);


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
        time[(count-1)]=content;
  	count++;
  	var flag=count-min;
  	if(flag==4)
  		$("#confirm_date").attr("disabled", "disabled");
  	
}

var SubmitComment=function (){
	event.preventDefault();
	var comment=$('#commentContent').val();
	$('#commentTable').append('<tr><td>'+comment+'</td><td>WANG WEI</td></tr>');
	$('#commentTable tr:last').after('<tr></tr>');
};
var submitForm=function (){
    //alert(typeof($("#input-name").val()));
    if($("#input-name").val()==""){
        document.getElementById('wrong').innerHTML = 'You have not set the event name!';
        $("#wrong").css('display', 'block');
        wrong[0]=1;
    }else{
        wrong[0]=0;
        $("#wrong").css('display', 'none');
    }
    if(wrong[0]==0){
        if($("#introduction").val()==""){
            document.getElementById('wrong').innerHTML = 'You have not set the introduction!';
            $("#wrong").css('display', 'block');
            wrong[1]=1;
        }else{
            wrong[1]=0;
            $("#wrong").css('display', 'none');
        }
    }
    if(wrong[1]==0){
    //alert(typeof(time[0]));
        if(time[0]==""){
            wrong[2]=1
            document.getElementById('wrong').innerHTML = 'You have not set the time!';
            $("#wrong").css('display', 'block');
        }else{
            wrong[2]=0;
            $("#wrong").css('display', 'none');
        }
    }
    if(wrong[2]==0){
        if($('#pac-input').val()==""){
            document.getElementById('wrong').innerHTML = 'You have not set the location!';
            $("#wrong").css('display', 'block');
            wrong[3]=1;
        }else{
            wrong[3]=0;
            $("#wrong").css('display', 'none');
        }
    }
    
    if(wrong[0]==0&&wrong[1]==0&&wrong[2]==0&&wrong[3]==0){
       $("#wrong").css('display', 'none');
       $.ajax({url:'/event/submit',
    type:'POST',
    data: {name:$("#input-name").val(), introduction:$("#introduction").val(), my1Time:time[0], my2Time:time[1], my3Time:time[2], location:$("#pac-input").val(), coordinate:coordinate}
       }).done(function (bal) {
    	alert(bal);
    	}).fail(function (jqXHR, textStatus) {
    	alert("Request failed: " + textStatus);
    	});
    }
};

$(document).ready(function() {
	var now = new Date();
	var day = ("0" + now.getDate()).slice(-2);
	var month = ("0" + (now.getMonth() + 1)).slice(-2);
	var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
	$('#selector').val(today);
        google.maps.event.addDomListener(window, 'load', initialize);
        $('#submitEvent').click(submitForm);
	
});
