import DS from 'ember-data';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';
import ENV from 'travels-front/config/environment'; 


export default DS.RESTAdapter.extend(DataAdapterMixin,{
	host: ENV.APP.backend_host,
	namespace: '/auth',
	contentType: 'application/json',
	dataType: 'json',
	authorizer: 'authorizer:token',


	buildURL: function(modelName, id, snapshot, requestType, query) {

		var url = this._super(modelName, id, snapshot, requestType, query);

		if (modelName === "account" && requestType === "createRecord"){
			url =this.get('host') +this.get('namespace')+"/register/";
		}
		else if (modelName === "profile") {
			url= this.get('host')+this.get('namespace')+'/me/detailed/';
		}

		//else if (modelName === "petition" && requestType === "createRecord") {
		//url = "http://127.0.0.1:8000/petition/user_petition/";
		//}

		return url;
	},
	normalizeErrorResponse: function(store, primaryModelClass, payload,id,requestType) {
		if (payload && typeof payload === 'object' && payload.errors) {
			return payload.errors;
		} else {
			var username='';
			if (payload.username!=null) {
				username=payload.username[0];
			}
			var email='';

			if (payload.email!=null) {
				email=payload.email[0];
			}

			return [
				{
					username: username,
					email: email
				}
			];
		}
	}



});


