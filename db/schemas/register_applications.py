def applications_schema(data, api_key, signature):
	document = {
		"app_name": data["app_name"], 
		"api_key": api_key,
		"redirect_uri": data["redirect_uri"],
		"user_group":[],
		"signature":signature,
		"enabled":True
	}	
	return document