var flag = 0;
var url="http://www.dungeonsanddevelopers.com/#";
var sex;
function validate_empty(obj) {
    if (obj.value == '') {
        flag = 1;
        return true;
    }
}
            function validate_range(obj) {
                var num = Number(obj.value);
                if ((num > 99) || (num < 0)) {
                    flag = 1;
                    return true;
                }
            }
            function validate_url(obj) {
                var str = obj.value;
                var n = str.length;
                var i = n;
                while (i > 0) {
                    if (str[0] == "#") {
                        BootstrapDialog.alert("You do not need to input '#' in the URL field!");
                        flag = 1;
                        return;
                    }
                    if (str.substring(0, i) == "http://www.dungeonsanddevelopers.com") {
                        BootstrapDialog.alert("You do not need to input http header and domain name in the URL field!");
                        flag = 1;
                        reutrn;
                    }
                    i--;
                }
            }
            function print_error() {
                var obj_name = document.getElementById("name");
                var obj_age = document.getElementById("age");
                var obj_years = document.getElementById("years");
                var obj_url = document.getElementById("url");
                var error_msg = '';
                if (validate_empty(obj_name))
				{
					$( "#name_field" ).highlight( "Name" );
					error_msg = [error_msg, "name"].join("");
				}else
					$( "#name_field" ).unhighlight( "Name" );
					
                if (validate_empty(obj_age)){
					$( "#age_field" ).highlight( "Age:" );
					error_msg = [error_msg, "age"].join(" ");
				}else
					$( "#age_field" ).unhighlight( "Age" );
                if (validate_empty(obj_years)){
					$( "#years_field" ).highlight( "Years of Web development:" );
					error_msg = [error_msg, "years"].join(" ");
				}else
					$( "#years_field" ).unhighlight( "Years of Web development:" );
                if (validate_empty(obj_url)){
					$( "#url_field" ).highlight( "Talent Tree URL:" );
					error_msg = [error_msg, "url"].join(" ");
				}else
					$( "#url_field" ).unhighlight( "Talent Tree URL:" );
                if (flag == 1) BootstrapDialog.alert(error_msg+" should be filled!");
                if (validate_range(age)) BootstrapDialog.alert("age should be within 0-99!");
                if (validate_range(years)) BootstrapDialog.alert("Number of years should be within 0-99!");
                validate_url(obj_url);
            }
			function view(){
				var sub_url=document.getElementById("url").value;
				location.href=[url,sub_url].join('');
			}
			function cancel(){
				$("#dialog-message").toggle();
			}
            function save_fuc() {
				flag=0;
                print_error();
                if (flag == 0) 
                    $("#dialog-message").toggle();
            }
        


			function save() {
				flag=0;
                print_error();
                if($('#male').attr("checked"))
					sex='Male';
				else if($('#female').attr("checked"))
					sex='Female';
                if(flag==0){
                	$("#dialog-message").toggle();
                	$("#name").attr("disabled", "disabled");
	              	$("#age").attr("disabled", "disabled");
	             	$("#years").attr("disabled", "disabled");
                	$("#url").attr("disabled", "disabled");
                	$("input:radio").attr("disabled", "disabled")
    				$.ajax({
    					url: '/submit/form', 
 						type: "POST",
 						data: {
 							name:$("#name").val(),
 							age:$("#age").val(),
 							years:$("#years").val(),
 							talent_url:$("#url").val(),
 							sex:sex
 							}
					});
    			}	
    		}
    		
	$(document).ready(function(){
			$('[name="mainForm"]').submit(function(event){
				event.preventDefault();
			});
	});