var count=1;
var coordinate='';
var time=["","",""];
var wrong=[0,0,0,0];
var flag;
var min=0;
//var initialeventid=$('#eventid').val();

var today='';
function submitComment(){
  event.preventDefault();
	var comment=$('#commentContent').val();
  var userName=$('#userName').val();
  var tempArray=today.split('T');
  var tempTime=tempArray[0]+" "+tempArray[1];
  //var commentTimeArray=today.split("T");
  //var commentTime=commentTimeArray[0]+" "+commentTimeArray[1];
  if($('#commentContent').val()=="")
    $("#commentwrong").css('display', 'block');
  else{
    $('#commentTable').prepend('<tr><td><span style="color:blue">'+userName+'</span>: '+escape(comment)+' </td><td>'+tempTime+'</td></tr>');
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
  alert("Cancel event!");
      //jConfirm('Your event has been cancelled!', 'Confirmation Dialog', function() {
      window.location.href="/home"; 
      //});
}
function setTime() {
	event.preventDefault();
  var timeDisplay=$('#datetime').val();
  //alert(test);
	//var content=$('#selector').val();
  //var timeArray=content.split("T");
  var length=$('#length').val();
  //showTime=timeArray[0]+" "+timeArray[1];
	var divIdName;
 	divIdName="my"+count+"Div";
  $('#timeContent').append(' <div id='+divIdName+' style="font-family:courier">'+count+'. '+timeDisplay+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  <a href="#" onclick="deleteTime(\'' + divIdName + '\')">   Delete</a></div>');
  time[(count-1)]=timeDisplay;
  alert(time[count-1]);
  count++;
  flag=count-min;
  
  if(flag>=4||length>=3){
  	$("#confirm_date").attr("disabled", "disabled");
    $("#datetime").attr("disabled", "disabled");
  }
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
      
      alert('Successfully create this event!');
      $("#submitEvent").attr("disabled", "disabled");
     // jConfirm('Successfully initial this event!', 'Confirmation Dialog', function() {
      window.location.href="/home"; 
 // });
    
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
  //if(votelength>=3){
  if($("#eventid").val().length!=0){
  	$("#confirm_date").attr("disabled", "disabled");
    $("#datetime").attr("disabled", "disabled");
  }
  //}
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
	//$('#selector').val(today);
  $('#submitEvent').click(submitForm);
  //$('#dateSelect').datetimepicker();
  var $j = jQuery.noConflict();
  $j("#datetime").datetimepicker();  
//<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
});
