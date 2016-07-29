import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	getModelForSave: Ember.computed(function() {
    return function(isSubmit) {
      if (isSubmit) {
      	let model = this.get("model");
      	let submit = this.get('store').createRecord("user-petition-submission", model.toJSON());

      	let petition_fields = ["project", "departure_point", "arrival_point", "task_start_date", "task_end_date"];

      	for (var field of petition_fields) {
      		submit.set(field, model.get(field));
      	};	
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
        return this.transitionToRoute("profile"); // TODO: redirect to submission view
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
