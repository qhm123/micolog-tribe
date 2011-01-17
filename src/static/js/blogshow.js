$(document).ready(function($){
	$('.showrate').each(function(){
		if($(this).attr("innerHTML").length > 0)
			return;
		$(this).raty({
		  start: $(this).attr("title"),
		  showHalf: true,
		  number: 5,
		  path: '/static/images/',
		  onClick: function(score){
		  	var id = $(this).attr("id");
		  	var blogid = $(this).attr("id").substring(5, id.length)
		    $.post(
		    	"/blogshow/rate",
		    	{ blogid: blogid, score: score },
		    	function(date){
		    	  if(date.success){
					  $("#rate_count-"+date.blogid).html(date.rate_count+"人投票");
					  $.fn.raty.start(date.rate, '#blog-'+date.blogid);
					  alert("投票成功");
				  }
				  else{
				  	$.fn.raty.start(date.rate, '#blog-'+date.blogid);
				  	alert("您已经透过票啦！");
				  }
				}
		    );
		  }
		});
	});
});