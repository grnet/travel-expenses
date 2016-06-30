import DS from 'ember-data';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';
import ENV from 'travels-front/config/environment'; 


export default DS.RESTAdapter.extend(DataAdapterMixin,{
	host: ENV.APP.backend_host,
	namespace: '/petition',
	contentType: 'application/json',
	dataType: 'json',
	authorizer: 'authorizer:token',
	user_related_models:['category','kind','specialty','tax-office'],



	buildURL: function(modelName, id, snapshot, requestType, query) {

		var url = this._super(modelName, id, snapshot, requestType, query);


		if (this.get('user_related_models').contains(modelName))
			this.set('namespace','/users_related');
		else
			this.set('namespace','/petition');

		if (requestType==="findRecord"){
			url=id;
		}
		if (requestType==="findAll"){
			url = this.get('host') +this.get('namespace')+"/"+modelName+"/";
		}
		if (requestType === "updateRecord"){

			url = id;
		}
		if (requestType === "createRecord"){
			url = url + "/";
		}
		if (requestType === "deleteRecord"){
			url = id;
		}
		if (requestType==="query"){
			url = this.get('host') +this.get('namespace')+"/"+modelName+"/";
		}

		if (modelName === "account" && requestType === "createRecord"){
			url =this.get('host') +'/auth'+'/register/';
		}

		return url;
	}




});


