$(document).ready(function(){
	$('#chat_input_button').click(function(){
		content = $('#chat_input').val()
		
		$.ajax({
			   type: "POST",
			   url: "/talk/send",
			   data: "content="+content,
			   success: function(msg){
			     $("#chat_transcript").load("/talk/history");
			   }
		});
	});
});