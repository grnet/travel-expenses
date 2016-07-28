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

      let model = this.get("model");
      let info_attrs = {"departure_point": model.get("departure_point.url"), "arrival_point": model.get("arrival_point.url")}
      let tinfo = this.get('store').createRecord("travel-info", info_attrs);
      let travel_info = [info_attrs]
      
      model.set("travel_info", travel_info);
      return this.get('model');
    }.bind(this);
  }),

	actions: {

		handleSubmit(e) {
      this.get('modelform').send('submit', e, true);
    }
  
  },	
});
