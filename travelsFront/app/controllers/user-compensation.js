import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	actions: {

		handleSubmit(e) {
      this.get('model').compensationSubmit().then(() => {
        this.transitionToRoute("petitionList");
      })
    },

    onSuccess(model) {
      if (model.constructor.modelName == "user-compensation-submission") {
        return this.transitionToRoute("petitionList");
      }
      this.transitionToRoute("userCompensation", model.get("id"));
    },

    onError(model) {
      let errors = model.get("errors");
      errors = _.groupBy(errors.toArray(), (e) => e.attribute);
      this.get("modelform.modelErrors").setProperties(errors);
    }
  
  },	
});
