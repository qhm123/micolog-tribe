$(document).ready(function($) {
	$('#cat_blogshow').click(function() {
		$('#content').load('/blogshow');
		anchorid = $(this).attr('id');
		select(anchorid);
	});
	$('#cat_rssa').click(function() {
		$('#content').load('/rssa');
		anchorid = $(this).attr('id');
		select(anchorid);
	});
	$('#cat_chat').click(function() {
		$('#content').load('/talk');
		anchorid = $(this).attr('id');
		select(anchorid);
	});
});

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