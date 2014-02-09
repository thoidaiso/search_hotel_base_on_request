
$( document ).ready(function() {
    $('#sort_hotel').change(function() {
    	csrf_token = $( "input[name='csrfmiddlewaretoken']" )[0].value
    	sort_type = this.value;
    	url = $(location).attr('href').replace($(location).attr('host'),'').replace('http://','')
    	setTimeout(sort_result_page(url, sort_type, csrf_token),3000);
	});
});




// jQuery(function($) {
	
	
	
	
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

// });