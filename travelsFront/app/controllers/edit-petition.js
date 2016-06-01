import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({
	
	editMessage:'',
	country_selected: false,
	arrivalPoints: null,

	actions: {
		
		setCountry(value){

			if (value!=='') {
				this.set('country_selected',true);

				let id=value.substring(value.indexOf('country/')+8,value.lastIndexOf('/'));
				let self=this;
				let movementID='';
				if (id == 10){
					movementID = 'http://127.0.0.1:8000/petition/movement_categories/1/';

					self.store.findRecord('movement-category', movementID).then(function(mc) {
						self.get('model').set('movementCategory',mc)		
					});
				}
				else{
					movementID = 'http://127.0.0.1:8000/petition/movement_categories/2/';

					self.store.findRecord('movement-category', movementID).then(function(mc) {
						self.get('model').set('movementCategory',mc)		
					});

				}
				self.store.query('city',{ country: id}).then(function(city){

					self.set('arrivalPoints',city);
					self.get('model').set('arrivalPoint',city);
				});
			}
			else
				this.set('country_selected',false);

		},

		petitionSave(){


			let profileIsValid=this.get('model.validations.isValid')

			if (profileIsValid) {

				var rec = this.store.peekRecord('petition-status',ENV.petition_status_1);
				this.get('model').set('status', rec);

				var self=this;
				this.get('model').save().then(function(value) {

					self.set('country_selected',false);
					self.set('editMessage','Τα στοιχεία της αίτησης σας έχουν αποθηκευθεί επιτυχώς !');
					Ember.$('#divMessage').removeClass('redMessage');
					Ember.$('#divMessage').addClass('greenMessage');

					let endDate=self.get('model.taskEndDate');
					if (endDate!==null) {

						endDate=endDate.replace('Z','');
						self.set('model.taskEndDate',endDate);
					}


					let startDate=self.get('model.taskStartDate');
					if(startDate!==null){

						startDate=startDate.replace('Z','');
						self.set('model.taskStartDate',startDate);
					}
				}, function(reason) {
					console.log("reason " + reason);
					console.log("Model id in after save " +  self.get('model.id'));
					self.set('editMessage','Η αποθήκευση των στοιχείων της αίτησης σας απέτυχε...');
					Ember.$('#divMessage').removeClass('greenMessage');
					Ember.$('#divMessage').addClass('redMessage');
					self.set('country_selected',false);

				});
			}
		},
		petitionSubmit(){


			let profileIsValid=this.get('model.validations.isValid')

			if (profileIsValid) {
				var rec = this.store.peekRecord('petition-status',ENV.petition_status_2);
				this.get('model').set('status', rec);
				
				var self=this;
				this.get('model').save().then(function(value) {

					self.set('editMessage','Τα στοιχεία της αίτησης σας έχουν υποβληθεί επιτυχώς !');
					Ember.$('#divMessage').removeClass('redMessage');
					Ember.$('#divMessage').addClass('greenMessage');
					self.transitionToRoute('petitionList');
					self.set('country_selected',false);
					
					let endDate=self.get('model.taskEndDate');
					if (endDate!==null) {

						endDate=endDate.replace('Z','');

						self.set('model.taskEndDate',endDate);
					}


					let startDate=self.get('model.taskStartDate');
					if(startDate!==null){
						startDate=startDate.replace('Z','');

						self.set('model.taskStartDate',startDate);
					}

				}, function(reason) {
					self.set('editMessage','Η υποβολή των στοιχείων της αίτησης σας απέτυχε...');
					Ember.$('#divMessage').removeClass('greenMessage');
					Ember.$('#divMessage').addClass('redMessage');
					self.set('country_selected',false);
					
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
			self.set('editMessage','');
			//Ember.$('#submit').prop('disabled', true);
		}
	}	
});
