function gotoResultPage(location, url, data)
	{
		
		console.log(url);
		data_arr = data.split('&');
		data = {};
		for (index = 0; index < data_arr.length; index++)
		{
			arr = data_arr[index].split('=');
			if (arr[0] == 'search_name')
				data['search_name'] = location;
			else
				data[ arr[0] ] = arr[1];
		}
		request_data = ""
		for( key in data)
		{
			request_data += key+ "=" + data[key] + '&'
		}
		
		href = url+ '?' + request_data;
		window.location.href = href;
	         
	}