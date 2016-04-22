import Ember from 'ember';

export default Ember.Controller.extend({

	actions: {

		petitionCreate(){

			var rec = this.store.peekRecord('petition-status', 'http://127.0.0.1:8000/petition/petition_status/1/');
			this.get('model').set('status', rec);
			console.log(rec.get('name'))

			let profileIsValid=this.get('model.validations.isValid')

			if (profileIsValid) {
				this.get('model').save();
			}
		},
		petitionSave(){

			var rec = this.store.peekRecord('petition-status', 2);
			this.get('model').set('petitionStatus', rec);

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

		setMovementCategory(id){
			var rec = this.store.peekRecord('movement-category', id);
			this.get('model').set('movementCategory', rec);

		},

		setTransportation(id){
			var rec = this.store.peekRecord('transportation', id);
			this.get('model').set('transportation', rec);

		},

		setProject(id){
			var rec = this.store.peekRecord('project', id);
			this.get('model').set('project', rec);

		},

		setSpecialty(id){
			var rec = this.store.peekRecord('specialty', id);
			this.get('model').set('specialtyID', rec);

		},

		setKind(id){
			var rec = this.store.peekRecord('kind', id);
			this.get('model').set('kind', rec);

		},
		setTaxOffice(id){
			var rec = this.store.peekRecord('tax-office', id);
			this.get('model').set('taxOffice', rec);

		}
	},	

});
