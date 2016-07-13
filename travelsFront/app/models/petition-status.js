import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr(),
	url: DS.attr(),
	statusID: Ember.computed('id', function(){
  	// return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  })
  
});
