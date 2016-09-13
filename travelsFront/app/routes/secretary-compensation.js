import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ENV from 'travels-front/config/environment'; 

const { get } = Ember;

export default Ember.Route.extend(AuthenticatedRouteMixin,{
	newPetition: true,
  modelName: 'secretary-compensation',

	model(params) {
    let petitionId = params.petition_id;
    let model;
    if (petitionId && petitionId != "new") {
      // edit petition
      model = this.store.findRecord(this.modelName, petitionId);
      this.set('newPetition', false);
    }
    return model;
	},

	actions: {
	}
	
});
