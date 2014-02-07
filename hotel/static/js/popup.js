/* 
	author: istockphp.com
*/
jQuery(function($) {
	
	$('#popup_tab a').click(function (e) {
	  e.preventDefault();
	  $(this).tab('show');
	})

	$("a.topopup").click(function() {
			hotel_id = $(this).attr('href');
			loading(hotel_id); // loading
			setTimeout(function(){ // then show popup, deley in .5 second
				loadPopup(); // function show popup 
			}, 500); // .5 second
	return false;
	});
	
	/* event for close the popup */
	$("div.close_popup").hover(
					function() {
						$('span.ecs_tooltip').show();
					},
					function () {
    					$('span.ecs_tooltip').hide();
  					}
				);
	
	$("div.close_popup").click(function() {
		disablePopup();  // function close pop up
	});
	
	$(this).keyup(function(event) {
		if (event.which == 27) { // 27 is 'Ecs' in the keyboard
			disablePopup();  // function close pop up
		}  	
	});
	
	$("div#toPopup").click(function() {
		disablePopup();  // function close pop up
	});
	
	$("div#popup_wrap").click(function() {
		popupContentClick = 1;
	});
	
	$('a.livebox').click(function() {
		alert('Hello World!');
	return false;
	});
	

	 /************** start: functions. **************/
	function loading(hotel_id) {
		$("div.loader").show();  
		
		 $.ajax({
             url: hotel_id,
             type: 'GET',
             success: function(response) {
             	$('#popup_content').html(response);
             	$('#carousel').flexslider({
				    animation: "slide",
				    controlNav: false,
				    animationLoop: false,
				    slideshow: false,
				    itemWidth: 100,
				    itemMargin: 20,
				    asNavFor: '#slider'
				  });
				   
				  $('#slider').flexslider({
				    animation: "slide",
				    controlNav: false,
				    animationLoop: false,
				    slideshow: false,
				    sync: "#carousel"
				  });
             }
             })
         
         
		
	}
	function closeloading() {
		$("div.loader").fadeOut('normal');  
	}
	
	
	var popupStatus = 0; // set value
	var popupContentClick = 0;
	
	function loadPopup() { 
		if(popupStatus == 0) { // if value is 0, show popup
			closeloading(); // fadeout loading
			$("#toPopup").fadeIn(0500); // fadein popup div
			$("#backgroundPopup").css("opacity", "0.7"); // css opacity, supports IE7, IE8
			$("#backgroundPopup").fadeIn(0001); 
			$('body').css('overflow','hidden');
			popupStatus = 1; // and set value to 1
		}	
	}
		
	function disablePopup() {
		if(popupStatus == 1 && popupContentClick == 0) { // if value is 1, close popup
			$("#toPopup").fadeOut("normal");  
			$("#backgroundPopup").fadeOut("normal");  
			$('body').css('overflow','auto');
			popupStatus = 0;  // and set value to 0
		}
		popupContentClick = 0;
	}
	/************** end: functions. **************/
}); // jQuery End