import DS from 'ember-data';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';


export default DS.RESTAdapter.extend(DataAdapterMixin,{
	host: 'http://127.0.0.1:8000',
	namespace: '/users_related',
	contentType: 'application/json',
	dataType: 'json',
	authorizer: 'authorizer:token',

	buildURL: function(modelName, id, snapshot, requestType, query) {

		var url = this._super(modelName, id, snapshot, requestType, query);

		if (modelName === "kind" && requestType==="findRecord"){
			url=id;
		}

		if (modelName === "kind" && requestType==="findAll"){
			url = "http://127.0.0.1:8000/users_related/kind/";

		}

		return url;
	} 

});

