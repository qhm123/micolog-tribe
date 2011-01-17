function toggleItemByID(id){
	var fid = 'entrycontent-' + id
	var fld = $('#' + fid);
	if(fld){
		fld.slideToggle(100);
		$('.postmetabottom').each(function(){
			if($(this).attr("id") != fid){
				$(this).slideUp(100);
			}
		});
	}
}

function toggleHotItemByID(id){
	var fid = 'hotentrycontent-' + id
	var fld = $('#' + fid);
	if(fld){
		fld.slideToggle(100);
		$('.postmetabottom').each(function(){
			if($(this).attr("id") != fid){
				$(this).slideUp(100);
			}
		});
	}
}

$(document).ready(function($){
	var ratethumb;
	$('.thumba').each(function(i){
		$(this).click(function(){
			ratethumb = $(this);
			var id = $(this).attr('id');
			var entryid;
			if(id.substring(0, 3) == "hot"){
				entryid = id.substring(11, id.length);
			}
			else{
				entryid = id.substring(8, id.length);
			}
			$.post(
				'/rssa/rate',
				{ entryid: entryid },
				function(data){
					if(data.success){
						ratethumb.addClass("thumbupclicked");
						span = ratethumb.next('span');
						span.text(('['+data.rate_count+'票]'));
					}
					else{
						alert("您已经投过票了");
					}
				}
			);
		});
	});
});