function select(anchorid) {
	$('#nav li a').each(function(i) {
		if ($(this).attr('id') == anchorid) {
			$(this).addClass("nav-selected");
		} else {
			$(this).removeClass("nav-selected");
		}
	});
}

$(document).ajaxStart(function() {
	$('#spinner').fadeIn();
}).ajaxStop(function() {
	$('#spinner').fadeOut();
});