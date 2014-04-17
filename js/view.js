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
    }
    i++;
  }  
}
function joinEvent(){
    saveVote();
     $.ajax({
    		url: "/event/submitvote", 
 				type: "POST",
 				data: {
         VoteList:chosenList,
         eventid:$("#eventid").val(),
          userid:$("#userid").val()
        }
      });
      //alert(chosenList);
}
$(document).ready(function() {
	var now = new Date();
	var day = ("0" + now.getDate()).slice(-2);
	var month = ("0" + (now.getMonth() + 1)).slice(-2);
	var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
	$('#selector').val(today);
        google.maps.event.addDomListener(window, 'load', initialize);
        //$('#submitEvent').click(submitForm);
	
});
