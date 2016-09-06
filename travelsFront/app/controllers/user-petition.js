import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	getModelForSave: Ember.computed(function() {
    return function(isSubmit) {
      if (isSubmit) {
      	let submit = this.get('model').cloneAs("user-petition-submission");
        return submit;
      }
      return this.get('model');
    }.bind(this);
  }),

	actions: {

		handleSubmit(e) {
      this.get('modelform').send('submit', e, true);
    },

    onSuccess(model) {
      if (model.constructor.modelName == "user-petition-submission") {
        return this.transitionToRoute("subPetitionList");
      }
      this.transitionToRoute("userPetition", model.get("id"));
    },

    onError(model) {
      let errors = model.get("errors");
      errors = _.groupBy(errors.toArray(), (e) => e.attribute);
      this.get("modelform.modelErrors").setProperties(errors);
    }
  
  },	
});
