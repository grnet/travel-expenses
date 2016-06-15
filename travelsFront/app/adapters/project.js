import DS from 'ember-data';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';
import ENV from 'travels-front/config/environment'; 


export default DS.RESTAdapter.extend(DataAdapterMixin,{
	host: ENV.APP.backend_host,
	namespace: '/petition',
	contentType: 'application/json',
	dataType: 'json',
	authorizer: 'authorizer:token',



	buildURL: function(modelName, id, snapshot, requestType, query) {

		var url = this._super(modelName, id, snapshot, requestType, query);

		if (modelName === "project" && requestType==="findRecord"){
			url=id;
		}
		if (modelName === "project" && requestType==="findAll"){
			url = this.get('host') +this.get('namespace')+"/project/";
		}

		return url;
	} 

});

