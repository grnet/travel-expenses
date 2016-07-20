import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices;

export var Petition = DS.Model.extend({
  dse: DS.attr(),
  first_name: DS.attr({attrs: {readonly: true}}),
  last_name: DS.attr(), 
  kind: DS.attr(),
  iban: DS.attr(),
	specialty: DS.attr({'label': 'Specialty', 'choices': CHOICES.SPECIALTY}),
  taxOffice: DS.belongsTo('tax-office'),
  taxRegNum: DS.attr({'label': 'VAT'}),
  category: DS.attr({'label': 'User Category'}),
  user: DS.belongsTo('profile'),
  taskStartDate: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
    label: 'Task starts at'
  }),
  taskEndDate: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
    label: 'Task ends at'
  }),
  travelInfo: DS.hasMany('travel-info'),
  project: DS.belongsTo('project'),
  reason: DS.attr(),
  petitionID: Ember.computed('id', function(){
    // return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  })
});

