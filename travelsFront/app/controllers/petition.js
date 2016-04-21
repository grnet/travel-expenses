import Ember from 'ember';

export default Ember.Controller.extend({

	actions: {

		petitionUpdate(){

			this.get('model').save();
		},

		setArrivalPoint(id){
			var rec = this.store.peekRecord('arrival-point', id);
			this.get('model').set('arrivalPoint', rec);

		},

		setDeparturePoint(id){
			var rec = this.store.peekRecord('departure-point', id);
			this.get('model').set('departurePoint', rec);

		},

		setCategoryOfTransport(id){
			var rec = this.store.peekRecord('movement-category', id);
			this.get('model').set('movementCategory', rec);

		},

		setMeanOfTransport(id){
			var rec = this.store.peekRecord('transportation', id);
			this.get('model').set('transportation', rec);

		},

		setProject(id){
			var rec = this.store.peekRecord('project', id);
			this.get('model').set('project', rec);

		}
	},	

});
