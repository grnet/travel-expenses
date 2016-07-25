import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	actions: {

		submitToState2(){
			let model = this.get("model");
			let submit = this.store.createRecord("user-petition-submission", model.toJSON());
			let petition_fields = ["project", "departure_point", "arrival_point"];

			for (var field of petition_fields) {
  			submit.set(field, model.get(field));
			};
			
			submit.save();
      } 
    },	
});
