import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	petitionMessage:'',
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
					movementID = ENV.APP.backend_host+'/petition/movement_categories/1/';

					self.store.findRecord('movement-category', movementID).then(function(mc) {
						self.get('model').set('movementCategory',mc)		
					});
				}
				else{
					movementID = ENV.APP.backend_host+'/petition/movement_categories/2/';

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

		let profileIsValid=this.get('model.validations.isValid');

			if (profileIsValid) {

				var rec = this.store.peekRecord('petition-status',ENV.petition_status_1);
				this.get('model').set('status', rec);

				var self=this;
				this.get('model').save().then(function(value) {
					
					self.set('petitionMessage','Τα στοιχεία της αίτησης σας έχουν αποθηκευθεί επιτυχώς !');
					self.set('petitionNotSaved',false);
					console.log('petitionNotSaved', self.get('petitionNotSaved'));
					Ember.$('#messageModal').modal();
					Ember.$('#styleModal').removeClass('btn-warning');
					Ember.$('#styleModal').addClass('btn-success');
					Ember.$('#submit').prop('disabled', false);

				}, function(reason) {
					self.set('petitionMessage','Η αποθήκευση των στοιχείων της αίτησης σας απέτυχε...');
					Ember.$('#messageModal').modal();
					Ember.$('#styleModal').removeClass('btn-success');
					Ember.$('#styleModal').addClass('btn-warning');
				});
			}
		},
		petitionSubmit(){

			let profileIsValid=this.get('model.validations.isValid');

			if (profileIsValid) {
				var rec = this.store.peekRecord('petition-status',ENV.petition_status_2);

				var self=this;

				self.get('model').set('status', rec);

				self.get('model').save().then(function(value) {

					self.set('petitionMessage','Τα στοιχεία της αίτησης σας έχουν υποβληθεί επιτυχώς !');
					self.set('petitionNotSaved',false);
					self.transitionToRoute('petitionList');
					// Ember.$('#messageModal').modal();
					// Ember.$('#styleModal').removeClass('btn-warning');
					// Ember.$('#styleModal').addClass('btn-success');

				}, function(reason) {

					self.set('petitionMessage','Η υποβολή των στοιχείων της αίτησης σας απέτυχε. Παρακαλούμε συμπληρώστε σωστά όλα τα στοιχεία της αίτησης');
					Ember.$('#messageModal').modal();
					Ember.$('#styleModal').removeClass('btn-success');
					Ember.$('#styleModal').addClass('btn-warning');
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
			//var self=this;
			//self.set('petitionMessage','');
			//self.set('petitionNotSaved',true);
			//Ember.$('#submit').prop('disabled', true);
		}
	},
});
