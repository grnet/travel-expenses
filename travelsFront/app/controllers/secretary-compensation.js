import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	actions: {

		handleSubmit(e) {
      this.get('model').compensationSubmit().then(() => {
        this.transitionToRoute("advancedList");
      })
    },

    onSuccess(model) {
      if (model.constructor.modelName == "secretary-compensation-submission") {
        return this.transitionToRoute("petitionList");
      }
      this.transitionToRoute("secretaryCompensation", model.get("id"));
    },

    onError(model) {
      let errors = model.get("errors");
      errors = _.groupBy(errors.toArray(), (e) => e.attribute);
      this.get("modelform.modelErrors").setProperties(errors);
    }
  
  },	
});

