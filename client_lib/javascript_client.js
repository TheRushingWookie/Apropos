function sanitize_tags(query, tag_map){
    /*Adjust query to use tags in tag_map.*/
    standardized_query = JSON.parse(JSON.stringify(query))
    for (var tag_index in query['input']){
        var tag = query['input'][tag_index]
        standard_tag = tag_map[tag]
        standardized_query['input'][standard_tag] =  query['input'][tag]
        //standardized_query['input'].pop(tag)
    }
    for (var tag_index in query['output']){
        var tag = query['input'][tag_index]
        standard_tag = tag_map[tag]
        standardized_query['output'][standard_tag] = query['output'][tag]
        //standardized_query['output'].pop(tag)
    }
    return query
}

function decide(responses){
    /*
    Iterates through all responses and returns the best response.
    Algorithm:
    1. hash each response for O(1) retrieval
    2. find key with largest value
    3. return the response corresponding to the key

    O(n) time with O(n) worst-case space
    */

    cache = {}

    // Fill up the hash table
    for (var response_index in responses){
        var response = responses[response_index]
        var output = response['output']
        if (cache[output] != undefined){
            cache[output] += 1
            }
        else{
            cache[output] = 1
        }
    }
    // Find the most common response from the cache
    final_response = undefined
    response_counter = 0
    for (var response_index in responses){
        var response = responses[response_index]
        if (cache[response] > response_counter)
        {
            final_response = response
            response_counter = cache[response]
        }
    }
    return final_response
    }
    var domain_name = "http://127.0.0.1:5000/"


function query(query, callback, target, wisdom, fast, authent){
    /*
    Example:
    query = {"action": "weather",
             "input": {"zip": 94539},
             "output": {"temperature": "int"}}
    */
    authent = (typeof authent === "undefined") ? "None" : authent;
    target = 0 || target;
    wisdom = 100 || wisdom;
    fast = false || fast;
    if (typeof (target) == "string"){
        query["mode"] = {"target": target}
    }
    else if(fast == true){
        wisdom = 1
        query["mode"] = {"wisdom": wisdom}
    }
    else if (typeof(wisdom) == "number"){
        query["mode"] = {"wisdom": wisdom}
    }
    else{
        console.log("Invalid Mode")
    }
    req = $.ajax({
        type: "POST",
        url: domain_name + "query",
        data: JSON.stringify(
        query),
        contentType: "application/json;",
        dataType: "json",
    });
    req.done(function( response ) {
     if (response){
        var tag_map = response['corrected_tags']
        query = sanitize_tags(query, tag_map)

        var urls = []
        console.log(response['apis'])
        for (var url_index = 0; url_index < response['apis'][0].length; url_index++){
            var url = response['apis'][0][url_index]
            urls.push(url)
        }

        var contents = []
        for (var url_index = 0; url_index < urls.length; url_index++){
            var url = urls[url_index]
            contents.push({'url': url, 'query': query})
        }

        if (query["mode"]['wisdom'] != undefined){
            var reqs = {}
            //Remember to do url uniqueness check later

            if (fast){

                for (var url_index in urls){
                        var url = urls[url_index]
                        reqs[url] = query_proxy(contents)
                        reqs[url].done(function(data) {
                        callback(JSON.stringify(data))
                    });
                    }

                return sanitize_tags(fastest_response, tag_map)
            }
            else{
                // Wisdom mode
                //alert(JSON.stringify(contents))
                for (var content_id in contents){
                        var content = contents[content_id]
                        reqs[url] = query_proxy(content)
                        reqs[url].done(function(data) {
                        callback(JSON.stringify(data))
                    });
                    }

                return decide(response)
                }
        }
        else if (typeof(target) == "string"){
            return false
        }
        return false;
     }
    else{
        return false
    }
      });
}
function query_proxy(content){
    /*
    Returns response from proxy.
    */
        //alert(JSON.stringify(content))
        console.log("querying")
        return $.ajax({
        type: "POST",
        url: content['url'] + '?json=',
        data: JSON.stringify(content['query']),
        contentType: "application/json;",
        crossDomain: true,
        dataType: "json",
})}
/*query({"action": "weather",
                 "input": {"city": 'Bethesda'},
                 "output": {"temperature": "int"}})*/
