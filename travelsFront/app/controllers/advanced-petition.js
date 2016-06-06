import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 


export default Ember.Controller.extend({
	petitionMessage:'',
	datesChanged:false,

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
		checkDates(){
			var self=this;
			var petition=self.get('model');


			if (petition.get('hasDirtyAttributes')) {

				var changed_attributes=petition.changedAttributes();
				console.log(changed_attributes);

				var dd=changed_attributes['depart_date'];
				var rd=changed_attributes['return_date'];
				var ted=changed_attributes['taskEndDate'];
				var tsd=changed_attributes['taskStartDate'];

				if (dd!=null) {
					var before=dd[0];
					var after=dd[1];
					if (before!=after) {
						self.set('datesChanged',true);
					}

				}
				if (rd!=null) {
					var before=rd[0];
					var after=rd[1];
					if (before!=after) {
						self.set('datesChanged',true);
					}
				}

				if (ted!=null) {
					var before=ted[0];
					var after=ted[1];
					if (before!=after) {
						self.set('datesChanged',true);
					}
				}

				if (tsd!=null) {
					var before=tsd[0];
					var after=tsd[1];
					if (before!=after) {
						self.set('datesChanged',true);
					}
				}
			}

		},

		petitionSave(){

			var self=this;

			let profileIsValid=self.get('model.validations.isValid');


			var petition=self.get('model');

			var a_petition=petition.get('advanced_info');
			var hotel=a_petition.get('accomondation');
			var flight=a_petition.get('flight');

			var ap_model=self.store.peekRecord('advanced-petition',a_petition.get('id'));

			var hotel_model=self.store.peekRecord('accommondation',hotel.get('id'));
			var flight_model=self.store.peekRecord('flight',flight.get('id'));

			var status = this.store.peekRecord('petition-status',ENV.petition_status_3);
			petition.set('status', status);

			if (profileIsValid) {

				//var rec = this.store.peekRecord('petition-status',ENV.petition_status_3);
				//self.get('model').set('status', rec);
				//

				hotel_model.save().then(function(hotel){
					flight_model.save().then(function(flight){


						ap_model.save().then(function(ap){
							petition.save().then(function(value) {
								self.set('petitionMessage','Τα στοιχεία της αίτησης έχουν αποθηκευθεί επιτυχώς !');
								self.set('petitionNotSaved',false);
								Ember.$('#divMessage').removeClass('redMessage');
								Ember.$('#divMessage').addClass('greenMessage');
								Ember.$('#submit').prop('disabled', false);


							}, function(reason) {
								self.set('petitionMessage','Η αποθήκευση των στοιχείων της αίτησης απέτυχε...');
								Ember.$('#divMessage').removeClass('greenMessage');
								Ember.$('#divMessage').addClass('redMessage');
							});

						});

					});

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
			self.set('petitionMessage','');
			//Ember.$('#submit').prop('disabled', true);
		}
	}	
});
