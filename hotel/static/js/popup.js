jQuery(function($) {
	
	$('#popup_tab a').click(function (e) {
	  e.preventDefault();
	  $(this).tab('show');
	})

	$("a.topopup").click(function() {
			hotel_id = $(this).attr('href');
			loading(hotel_id); // loading
			setTimeout(function(){ // then show popup, delay in .5 second
				loadPopup(); // function show popup 
			}, 500); // .5 second
	return false;
	});
	
	// Load statistic info
	$('#statistic').click(function(){
		url = $(location).attr('href').replace($(location).attr('host'),'').replace('http://','').replace('/get_result/?','');
		loading_statistic(url); // loading
		setTimeout(function(){ // then show popup, delay in .5 second
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
	function loading_statistic(url){
		$("div.loader").show();  
		
		data_post = {}
		
		url_arr = url.split('&');
		for (var i =0; i< url_arr.length; i++)
		{
			arr = url_arr[i].split('=');
			if (arr.length == 2)
			{
				data_post[arr[0]] = arr[1]
			}
		}
		console.log(url);
		console.log(data_post);
		
		 $.ajax({
             url: 'statistic',
             type: 'GET',
             data: data_post,
             success: function(response) {
             	$('#popup_content').html(response);
             }
             })
	}
	
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
	
	// POST page number to change pagination in  /get_result

function changeResultPage(url, page, csrf_token)
	{
		jQuery.ajax({
	         url: url,
	         type: 'POST',
	         data: {
	         		'page': page,
	         		csrfmiddlewaretoken: csrf_token,
	         	},
	         success: function(data)
	         		{
	         			$("#result_column").html(data);
	         		}
	         });
	         
	}
