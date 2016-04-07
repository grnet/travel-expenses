import DS from 'ember-data';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';


export default DS.RESTAdapter.extend(DataAdapterMixin,{
	host: 'http://127.0.0.1:8000',
	namespace: '/auth',
	contentType: 'application/json',
	dataType: 'json',
	authorizer: 'authorizer:token',
	
	// headers: {
	// 	withCredentials: true,
	// 	"X-CSRFToken": 'qrxKb6Tn5C6JCj8EllYst2tsJqUfE3tT',
	// 	username: 'admin',
 //    	password: 'admin'
 //    },



    buildURL: function(modelName, id, snapshot, requestType, query) {

		var url = this._super(modelName, id, snapshot, requestType, query);
	
      	if (modelName === "account" && requestType === "createRecord"){
      		url = "http://127.0.0.1:8000/auth/register/";
      	}
      	else if (modelName === "profile") {
      		url = "http://127.0.0.1:8000/auth/me/detailed/";
      	}
      	else if (modelName === "specialty") {
      		url = "http://127.0.0.1:8000/users_related/kind/";
      	}

      	return url;
    } 
   
});


