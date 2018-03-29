import DS from 'ember-data';
import Ember from 'ember';

export default DS.Model.extend({
  __api__: {
    path: 'tax-office',
  },
  full_label: Ember.computed('name', function(){
    return this.get('name');
  }),
  name:  DS.attr(),
  description:  DS.attr(),
  address:  DS.attr(),
  email:  DS.attr(),
  phone:  DS.attr(),
  url: DS.attr(),
});
