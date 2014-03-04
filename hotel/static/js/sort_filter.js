
$( document ).ready(function() {
    $('#sort_hotel').change(function() {
    	csrf_token = $( "input[name='csrfmiddlewaretoken']" )[0].value;
    	sort_type = this.value;
    	url = $(location).attr('href').replace($(location).attr('host'),'').replace('http://','');
    	setTimeout(sort_result_page(url, sort_type, csrf_token),3000);
	});
	
	$('#export_to_csv').click(function()
	{
		csrf_token = $( "input[name='csrfmiddlewaretoken']" )[0].value;
		url = $(location).attr('href').replace($(location).attr('host'),'').replace('http://','');
		$("body").append('<iframe src="'+url+'&export_type=csv" style="display: none;" ></iframe>');

	}
	)
	
	$('#export_to_pdf').click(function()
	{
		csrf_token = $( "input[name='csrfmiddlewaretoken']" )[0].value;
		url = $(location).attr('href').replace($(location).attr('host'),'').replace('http://','');
		$("body").append('<iframe src="'+url+'&export_type=pdf" style="display: none;" ></iframe>');

	}
	)
	
	$("[id*='search_star_rating_']").change(function(){
		setTimeout( $("#btn_search").click(),3000);
	})
	
	$("[id*='search_facility']").change(function(){
		setTimeout( $("#btn_search").click(),3000);
	})
	
	$("#search_hotelname").keypress(function(event){
		console.log(event.keyCode);
	    if(event.keyCode == 13){
	    	event.preventDefault();
	        $("#btn_search").click();
	    }
	});
	
	// $('#search_hotelname_btn').click(function(){
		// console.log("handle filter---")
		// csrf_token = $( "input[name='csrfmiddlewaretoken']" )[0].value;
		// url = $(location).attr('href').replace($(location).attr('host'),'').replace('http://','')
// 		
		// type_filter = 'name';
		// filter_content = $('#search_hotelname')[0].value;
		// filter_result_page(url, type_filter, filter_content, csrf_token);
	// });
	
	

});




function sort_result_page(url, sort_type, csrf_token)
{
	console.log(url);
	console.log(sort_type);
	// alert(12);
	// console.log(this.value)
	jQuery.ajax({
         url: url,
         type: 'POST',
         data: {
         		'sort_type': sort_type,
         		csrfmiddlewaretoken: csrf_token,
         	},
         success: function(data)
         		{
         			$("#result_column").html(data);
         		}
         });
}
