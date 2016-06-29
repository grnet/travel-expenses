import DS from 'ember-data';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';
import ENV from 'travels-front/config/environment'; 


export default DS.RESTAdapter.extend(DataAdapterMixin,{
	host: ENV.APP.backend_host,
	namespace: 'petition/advanced_petition',
	contentType: 'application/json',
	dataType: 'json',
	authorizer: 'authorizer:token',


	pathForType: function(modelName) {
		var decamelized = Ember.String.decamelize(modelName);
		return "";
	},
	buildURL: function(modelName, id, snapshot, requestType, query) {

		var url = this._super(modelName, id, snapshot, requestType, query);

		if (requestType === "createRecord"){
			url = url + "/";
		}
		if (requestType === "deleteRecord"){
			url = id;
		}
		if (requestType === "updateRecord"){
			url = id;
		}
		if (requestType === "findRecord"){
			url = id;
		}

		return url;
	} 

});
