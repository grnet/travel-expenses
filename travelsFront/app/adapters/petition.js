import DS from 'ember-data';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';


export default DS.RESTAdapter.extend(DataAdapterMixin,{
	host: 'http://127.0.0.1:8000',
	namespace: 'petition/user_petition',
	contentType: 'application/json',
	dataType: 'json',
	authorizer: 'authorizer:token',


	pathForType: function(modelName) {
		var decamelized = Ember.String.decamelize(modelName);
		return "";
	},
	buildURL: function(modelName, id, snapshot, requestType, query) {

		var url = this._super(modelName, id, snapshot, requestType, query);
		console.log(requestType, "requestType")
		if (requestType === "createRecord"){
			url = url + "/";
		}
		if (requestType === "deleteRecord"){
			url = id;
		}
		if (requestType === "findRecord"){
			url = id;
		}

		return url;
	} 

});
