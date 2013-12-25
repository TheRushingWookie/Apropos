
function query(query) {
	var domain_name = "http://localhost:5000/";
	var url = domain_name.concat("query?action=");
	var input_url = "";
	var output_url = "";
	var action = query["action"];

	var inputs = query["input"].keys;
	for (var i = 0; i < inputs.length; i++) {
		input_url = input_url.concat(encodeURIComponent("&input=".concat(inputs[i])));
	}

	var outputs = query["output"].keys;
	for (var i = 0; i < outputs.length; i++) {
		output_url = output_url.concat(encodeURIComponent("&input=".concat(outputs[i])));
	}

	url = url.concat(action.concat(input_url.concat(output_url)));
	// print url here
	var xhr = new XMLHttpRequest();
	xhr.open('POST', url, false);  # third param is sync/async
	xhr.send(data);
	var response = xhr.responseText;
	var response = urllib2.urlopen(url)

	response = response.read()
	response =  urllib2.unquote(response)
	response = json.loads(response)
	print response
	print "Response is " + str(response['apis'][0][0])
	url = response['apis'][0][0]
	query_proxy(url,query)
}