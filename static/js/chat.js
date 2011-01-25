onOpened = function(){
	$.ajax({
		type: "POST",
		url: "/talk/online",
		success: function(msg){
		}
	});
}

onMessage = function(m){
	$("#chat_transcript").load("/talk/history");
}

onError = function(error){
	alert('Error. description:' + error.description + 'code:' + error.code);
}

onClose = function(){
	alert('closed!');
	$.ajax({
		type: "POST",
		url: "/talk/offline",
		success: function(msg){
		}
	});
}

function isNull(str){
	if (str == "") return true;
	var regu = "^[ ]+$";
	var re = new RegExp(regu);
	return re.test(str);
}

$(document).ready(function(){
	layout();
	$("#chat_transcript").scrollTop($("#chat_transcript")[0].scrollHeight);
	
	channel = new goog.appengine.Channel(talk_token);
	socket = channel.open();
	socket.onopen = onOpened;
	socket.onmessage = onMessage;
	socket.onerror = onError;
	socket.onclose = onClose;
	
	$('#chat_input_button').click(function() {
		chat_input = $('#chat_input');
		if(chat_input){
			content = chat_input.val();
			if (isNull(content)){
				alert('请输入内容！');
			}
			else{
				$.ajax({
					type : "POST",
					url : "/talk/send",
					data : "content=" + content,
					success : function(msg) {
						$("#chat_transcript").load("/talk/history");
						$('#chat_input').val('');
						$("#chat_transcript").scrollTop($("#chat_transcript")[0].scrollHeight);
					}
				});
			}
		}
	});
	
});

$(window).resize(function() {
	layout();
});

function layout() {
	if ($('#group') != null) {
		resizeContentHeight('#group', ['#group_chat_container']);
	}
}

function resizeContentHeight(element_name, dependents, offsets) {
	if (dependents == undefined) {
		dependents = [];
	}
	// 距离底部偏移
	var offset = 252;
	var parent = $(element_name);
	var height = window.innerHeight
			|| (window.document.documentElement.clientHeight || window.document.body.clientHeight);
	var desired_height = offset;
	if (height > offset) {
		desired_height = (height - offset);
	}
	var parent_offset = 0;
	if (dependents.length > 0) {
		var transcript = $('#chat_transcript');
		var container_height = $('#group_chat_container').height();
		if (container_height != (desired_height - parent_offset)) {
			container_height = (desired_height - parent_offset);
		}
		var input_height = $('#chat_input_container').height();
		var transcript_offset = 12;
		new_height = (container_height - input_height) - transcript_offset;
		if (transcript.height() != new_height && new_height > 0) {
			transcript.height((container_height - input_height)
					- transcript_offset + 'px');
		}
	}
	$.each(dependents, function(n, item) {
		child_element = $(item);
		if (child_element.height() != (desired_height - parent_offset)) {
			child_element.height((desired_height - parent_offset) + 'px');
		}
	});
	if (parent.height() != (height - offset)) {
		parent.height((desired_height) + 'px');
	}
}