import Ember from 'ember';

export default Ember.Controller.extend({

	profileMessage:'',

	init: function(){
		this._super();	
		let userCategory = 'http://127.0.0.1:8000/users_related/category/2/';
		var rec = this.store.findRecord('category', userCategory);
		this.set('category',rec);		
  	},

	actions: {

		profileUpdate(){
			let profileIsValid=this.get('model.validations.isValid');

			// console.log(this.get('models.validations.attrs.username.messages'))
			if (profileIsValid) {

				var self=this;
				this.get('model').save().then(function(value) {
					self.set('profileMessage','Τα στοιχεία του προφίλ σας έχουν αποθηκευθεί επιτυχώς !');
					Ember.$('#messageModal').modal();
					Ember.$('#styleModal').removeClass('btn-warning');
					Ember.$('#styleModal').addClass('btn-success');

				}, function(reason) {
					self.set('profileMessage','Η αποθήκευση των στοιχείων του προφίλ σας απέτυχε...');
					Ember.$('#messageModal').modal();
					Ember.$('#styleModal').removeClass('btn-success');
					Ember.$('#styleModal').addClass('btn-warning');

				});
			}
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
			this.get('model').set('category', rec);

		},
		clearMessage(){
			var self=this;
			self.set('profileMessage','');
		}

	},


});
