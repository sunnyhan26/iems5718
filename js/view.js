var count=1;
var coordinate='';

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
var chosenList=new Array(3);
function saveVote(){
  var i=0;
  while (i<3){
    var radioName="radio"+i+"Name";
    //alert(radioName);
    if($("#"+radioName).length>0){
      var radioObj = document.getElementById(radioName);
      if(radioObj.checked){
        chosenList[i]=1;
      }
      else{
        chosenList[i]=0;
      }
    }else
      chosenList[i]=0;
    i++;
  }  
}
var today='';
function submitComment(){
  event.preventDefault();
	var comment=$('#commentContent').val();
  var userName=$('#userName').val();
  
  alert(comment);
  $('#commentTable').append('<tr><td>'+userName+': '+comment+' </td></tr>');
	$('#commentTable').append('<tr><td>'+today+'</td><td>WANG WEI</td></tr>');
	$('#commentTable tr:last').after('<tr></tr>');
  $.ajax({
    url:'/comments/add',
    type:'POST',
    data:{
      comment:$('#commentContent').val(),
      eventid:$("#eventId").val(),
    }
  });
}
function joinEvent(){
  saveVote();
  var firstVote=chosenList[0];
  var secVote=chosenList[1];
  var thirdVote=chosenList[2];
  alert(firstVote);
  $.ajax({
    		url: "/event/submitvote", 
 				type: "POST",
 				data: {
          firstVote:firstVote,
          secVote:secVote,
          thirdVote:thirdVote,
          eventid:$("#eventId").val(),
        }
      });
  alert("Successfully join this event!");
  $("#join").attr("disabled", "disabled");
  window.location.href="/home"; 
      //alert(chosenList);
}
$(document).ready(function() {
	var now = new Date();
	var day = ("0" + now.getDate()).slice(-2);
	var month = ("0" + (now.getMonth() + 1)).slice(-2);
  today = now.getFullYear()+"-"+(month)+"-"+(day) ;
  
	$('#selector').val(today);
        google.maps.event.addDomListener(window, 'load', initialize);
        //$('#submitEvent').click(submitForm);
	
});
