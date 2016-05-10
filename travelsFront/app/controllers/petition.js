import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	message:'',
	statePetition:'',
	now: Ember.computed(function() {
		return moment().format("YYYY-MM-DDTHH:mm:ssZ");

	}),
	country_selected: false,
	arrivalPointModel: null,


	actions: {

		setCountry(value){

			if (value!=='') {
				this.set('country_selected',true);

				let id=value.substring(value.indexOf('country/')+8,value.lastIndexOf('/'));
				var city=this.store.query('city',{ country: id});
				this.set('arrivalPointModel',city);
				this.get('model').set('arrivalPoint',city);
			}
			else
				this.set('country_selected',false);

		},

		petitionSave(){


			let profileIsValid=this.get('model.validations.isValid')

			if (profileIsValid) {
				//this.get('model').save();

				var rec = this.store.peekRecord('petition-status',ENV.petition_status_1);
				var pet_name=this.get('profile.first_name');	
				var pet_surname=this.get('profile.last_name');
				var pet_iban=this.get('profile.iban');
				var pet_specialty=this.get('profile.specialtyID');
				var pet_kind=this.get('profile.kind');
				var pet_taxNum=this.get('profile.taxRegNum');
				var pet_taxOffice=this.get('profile.taxOffice');


				this.get('model').set('status', rec);
				this.get('model').set('name', pet_name);
				this.get('model').set('surname',pet_surname);
				this.get('model').set('iban', pet_iban);
				this.get('model').set('specialtyID', pet_specialty);
				this.get('model').set('kind', pet_kind);
				this.get('model').set('taxRegNum', pet_taxNum);
				this.get('model').set('taxOffice', pet_taxOffice);
				let now=this.get('now');
				this.get('model').set('creationDate',now);
				this.get('model').set('updateDate',now);

				/*let endDate=this.get('model').get('taskEndDate');*/
				//console.log("Enddate:"+endDate);
				//endDate=moment(endDate).format("YYYY-MM-DDTHH:mm:ss");
				//console.log("Formated enddate:"+endDate);
				/*this.get('model').set('taskEndDate',endDate);*/


				this.get('model').set('status', rec);

				var self=this;
				this.get('model').save().then(function(value) {
					self.set('statePetition', true);
					self.set('message','Τα στοιχεία της αίτησης σας έχουν αποθηκευθεί επιτυχώς !');

					self.transitionToRoute('petitionList');

				}, function(reason) {
					self.set('statePetition', false);
					self.set('message','Η αποθήκευση των στοιχείων της αίτησης σας απέτυχε...');

				});
			}
		},
		petitionSubmit(){


			let profileIsValid=this.get('model.validations.isValid')

			if (profileIsValid) {
				//this.get('model').save();
				var rec = this.store.peekRecord('petition-status',ENV.petition_status_2);

				var pet_name=this.get('profile.first_name');	
				var pet_surname=this.get('profile.last_name');
				var pet_iban=this.get('profile.iban');
				var pet_specialty=this.get('profile.specialtyID');
				var pet_kind=this.get('profile.kind');
				var pet_taxNum=this.get('profile.taxRegNum');
				var pet_taxOffice=this.get('profile.taxOffice');


				this.get('model').set('status', rec);
				this.get('model').set('name', pet_name);
				this.get('model').set('surname',pet_surname);
				this.get('model').set('iban', pet_iban);
				this.get('model').set('specialtyID', pet_specialty);
				this.get('model').set('kind', pet_kind);
				this.get('model').set('taxRegNum', pet_taxNum);
				this.get('model').set('taxOffice', pet_taxOffice);
				let now=this.get('now');
				this.get('model').set('creationDate',now);
				this.get('model').set('updateDate',now);



				var self=this;
				this.get('model').save().then(function(value) {

					self.set('message','Τα στοιχεία της αίτησης σας έχουν υποβληθεί επιτυχώς !');
					self.set('statePetition', true);
					self.transitionToRoute('petitionList');
				}, function(reason) {

					self.set('message','Η υποβολή των στοιχείων της αίτησης σας απέτυχε...');
					self.set('statePetition', false);
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
