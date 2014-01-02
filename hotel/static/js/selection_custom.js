$(document).ready(function(){
			
	/* ---- */
	/* FORM */
	/* ---- */
	$('.search_filter_heading')
		.click(
			function() {
				
				
				parent = $(this).parent();
				
				block_search = parent.find('#block_search');
				
				if ($(block_search).hasClass('close')) {
					
					$(block_search).removeClass('close');
					$(block_search).slideDown(1000);
					return false;
				} else {
					
					$(block_search).addClass('close');
					$(block_search).slideUp(150);
					
					
					return false;
				}
				
				return false;
			}
		)
	$('.dropdown')
		.click( 
			function() {
				$(this).children('ul').slideToggle(150);
				
				if ($(this).hasClass('open')) {
					$(this).removeClass('open');
					return false;
				} else {
					$(this).addClass('open');
					return false;
				}
				
				return false;
			})
			
		.hover( 
			function() {
			
			},
			function() {
				$(this).children('ul').slideUp(150);
				$(this).removeClass('open');
			});
		
	$('.dropdown ul li')
		.click( 
			function() {
				var sitem = $(this).html();
				var sid = $(this).attr('id');
				
				$(this).siblings('li').removeClass('selected');
				$(this).addClass('selected');
				$(this).parent('ul').siblings('span.selected').html(sitem);
				$(this).parent('ul').siblings('input').val(sid);
			});
			

});
/* end document ready */
	


