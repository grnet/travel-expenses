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
    }
  
  },	
});
