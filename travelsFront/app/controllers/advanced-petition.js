import Ember from 'ember';

export default Ember.Controller.extend({

	country_selected: false,
	arrivalPoints: null,
	categoryOfMovement: null,

	actions: {

		setCountry(value){

			if (value!=='') {
				this.set('country_selected',true);

				let id=value.substring(value.indexOf('country/')+8,value.lastIndexOf('/'));
				if (id == 10){
					let movementID = 'http://127.0.0.1:8000/petition/movement_categories/1/';
					var rec = this.store.findRecord('movement-category', movementID);
					this.set('categoryOfMovement',rec);
					this.get('model').set('movementCategory',rec)		
				}
				else{
					let movementID = 'http://127.0.0.1:8000/petition/movement_categories/2/';
					var rec = this.store.findRecord('movement-category',movementID);
					this.set('categoryOfMovement',rec);
					this.get('model').set('movementCategory',rec);					
				}
				var city=this.store.query('city',{ country: id});
				this.set('arrivalPoints',city);
				this.get('model').set('arrivalPoint',city);
			}
			else
				this.set('country_selected',false);

		},

		setArrivalPoint(id){
			var rec = this.store.peekRecord('city', id);
			this.get('model').set('arrivalPoint', rec);

		},

		setDeparturePoint(id){
			var rec = this.store.peekRecord('city', id);
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
		setFeeding(id){
			var rec = this.store.peekRecord('feeding', id);
			this.get('model').set('feeding', rec);

		},

		setTaxOffice(id){
			var rec = this.store.peekRecord('tax-office', id);
			this.get('model').set('taxOffice', rec);

		},
		setCategory(id){
			var rec = this.store.peekRecord('category', id);
			this.get('model').set('user_category', rec);

		},
		clearMessage(){
			var self=this;
			self.set('editMessage','');
			//Ember.$('#submit').prop('disabled', true);
		}
	}	
});
