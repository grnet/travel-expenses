import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	petitionMessage:'',
	// now: Ember.computed(function() {
	// 	return moment().format("YYYY-MM-DDTHH:mm:ssZ");

	// }),
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

		petitionSave(){


			let profileIsValid=this.get('model.validations.isValid');

			if (profileIsValid) {

				var rec = this.store.peekRecord('petition-status',ENV.petition_status_1);
				this.get('model').set('status', rec);

				// let now=this.get('now');
				// this.get('model').set('creationDate',now);
				// this.get('model').set('updateDate',now);

				var self=this;
				this.get('model').save().then(function(value) {
					self.set('petitionMessage','Τα στοιχεία της αίτησης σας έχουν αποθηκευθεί επιτυχώς !');
					self.set('petitionNotSaved',false);
					Ember.$('#divMessage').removeClass('redMessage');
					Ember.$('#divMessage').addClass('greenMessage');
					Ember.$('#submit').prop('disabled', false);

				}, function(reason) {
					self.set('petitionMessage','Η αποθήκευση των στοιχείων της αίτησης σας απέτυχε...');
					Ember.$('#divMessage').removeClass('greenMessage');
					Ember.$('#divMessage').addClass('redMessage');
				});
			}
		},
		petitionSubmit(){


			let profileIsValid=this.get('model.validations.isValid');

			if (profileIsValid) {
				var rec = this.store.peekRecord('petition-status',ENV.petition_status_2);


				this.get('model').set('status', rec);
				// let now=this.get('now');
				// this.get('model').set('creationDate',now);
				// this.get('model').set('updateDate',now);

				var self=this;
				this.get('model').save().then(function(value) {

					self.set('petitionMessage','Τα στοιχεία της αίτησης σας έχουν υποβληθεί επιτυχώς !');
					Ember.$('#divMessage').removeClass('redMessage');
					Ember.$('#divMessage').addClass('greenMessage');
					self.transitionToRoute('petitionList');
				}, function(reason) {

					self.set('petitionMessage','Η υποβολή των στοιχείων της αίτησης σας απέτυχε...');
					Ember.$('#divMessage').removeClass('greenMessage');
					Ember.$('#divMessage').addClass('redMessage');
				});
			}
		},
		setArrivalPoint(id){
			var rec = this.store.peekRecord('city', id);
			this.get('model').set('arrivalPoint', rec);

		},

		setDeparturePoint(id){
			var rec = this.store.peekRecord('city', id);
			this.get('model').set('departurePoint', rec);
					
		},

		//setMovementCategory(id){
		//	var rec = this.store.peekRecord('movement-category', id);
		//	this.get('model').set('movementCategory', rec);
		//},

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

		},
		setCategory(id){
			var rec = this.store.peekRecord('category', id);
			this.get('model').set('user_category', rec);

		},
		clearMessage(){
			var self=this;
			self.set('petitionMessage','');
			self.set('petitionNotSaved',true);
			Ember.$('#submit').prop('disabled', true);
		}
	},
		

});
