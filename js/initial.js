var count=1;
var coordinate='';
var time=["","",""];
var wrong=[0,0,0,0];
var flag;
var min=0;
//var initialeventid=$('#eventid').val();
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
var today='';
function submitComment(){
  event.preventDefault();
	var comment=$('#commentContent').val();
  var userName=$('#userName').val();
  var tempArray=today.split('T');
  var tempTime=tempArray[0]+" "+tempArray[1];
  //var commentTimeArray=today.split("T");
  //var commentTime=commentTimeArray[0]+" "+commentTimeArray[1];
  
  $('#commentTable').prepend('<tr><td><span style="color:blue">'+userName+'</span>: '+comment+' </td><td>'+tempTime+'</td></tr>');
	//$('#commentTable tr:first').after('<tr></tr>');
 $('#commentContent').removeAttr('value');
  $.ajax({
    url:'/comments/add',
    type:'POST',
    data:{
      comment:$('#commentContent').val(),
      eventid:$('#eventid').val(),
    }
  });
}
function deleteTime(divNum) {
	event.preventDefault();
	$('#'+divNum).remove();
	flag--;
	if(flag<4)
  		$("#confirm_date").removeAttr('disabled');
}
function cancel(){
  //alert("Do you really want to cancel it?");
  $.ajax({
    url:'/event/cancel',
    type:'POST',
    data:{
      eventid:$('#eventid').val(),
    }
  });
      jConfirm('Your event has been cancelled!', 'Confirmation Dialog', function() {
      window.location.href="/home"; 
      });
}
function setTime() {
	event.preventDefault();
	var content=$('#selector').val();
  var timeArray=content.split("T");
  var length=$('#length').val();
  showTime=timeArray[0]+" "+timeArray[1];
	var divIdName;
 	divIdName="my"+count+"Div";
  $('#timeContent').append(' <div id='+divIdName+'>'+showTime+'<a href="#" onclick="deleteTime(\'' + divIdName + '\')">   Delete</a></div>');
  time[(count-1)]=showTime;
  //alert(time[count-1]);
  count++;
  flag=count-min;
  
  if(flag>=4||length>=3)
  	$("#confirm_date").attr("disabled", "disabled");
  	
}

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
        if($('#timeContent').is(':empty')){
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
        data: {
          name:$("#input-name").val(), 
          introduction:$("#introduction").val(), 
          my1Time:time[0], 
          my2Time:time[1], 
          my3Time:time[2], 
          location:$("#pac-input").val(), 
          coordinate:coordinate,
          eventid:$('#eventid').val(),
        }
      });
      jAlert('Successfully create this event!');
      $("#submitEvent").attr("disabled", "disabled");
      jConfirm('Successfully initial this event!', 'Confirmation Dialog', function() {
      window.location.href="/home"; 
  });
    
   }
 
};

$(document).ready(function() {
  //alert(length);

  if($("#eventid").val().length!=0){
    $("#commentArea").show();
    $("#cancelEvent").show();
  }
  else{
    $("#commentArea").hide();
    $("#cancelEvent").hide();
  }
  var votelength=$("#length").val();
  if(votelength>=3)
  	$("#confirm_date").attr("disabled", "disabled");
	var date = new Date;
  //date.setTime(result_from_Date_getTime);
  var seconds = date.getSeconds();
  var minutes = date.getMinutes();
  var hour = date.getHours();
  var year = date.getFullYear();
  var month = date.getMonth()+1; // beware: January = 0; February = 1, etc.
  var day = date.getDate();
  month="0" + month;
  if(minutes<10)
    minutes="0"+minutes;
  if(hour<10)
    hour="0"+hour;
  

  today = year+"-"+month+"-"+day+"T"+hour+":"+minutes;
 // alert(today);
	$('#selector').val(today);
  google.maps.event.addDomListener(window, 'load', initialize);
  $('#submitEvent').click(submitForm);
	
});
