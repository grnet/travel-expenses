import DS from 'ember-data';

export default DS.RESTAdapter.extend({

	host: 'http://127.0.0.1:8000',
	namespace: '/auth',
	contentType: 'application/json',
	dataType: 'json',
	
	headers: {
		withCredentials: true,
		"X-CSRFToken": 'qrxKb6Tn5C6JCj8EllYst2tsJqUfE3tT',
		username: 'admin',
    	password: 'admin'
    },



    buildURL: function(modelName, id, snapshot, requestType, query) {

		var url = this._super(modelName, id, snapshot, requestType, query);
	
      	if (requestType === "createRecord"){
      		url = "http://127.0.0.1:8000/auth/register/";
      	}
      	else if (requestType === "findAll"){
      		url = "http://127.0.0.1:8000/auth/login/";
      	}

      	return url;
    } 
   
});
