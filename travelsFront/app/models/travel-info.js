import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment';

const CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({
  __api__: {
    ns: 'petition'
  },
  url: DS.attr(),
  departure_point: DS.belongsTo('city', {attrs: {required: true}}),
  arrival_point: DS.belongsTo('city', {attrs: {required: true}}),
  // depart_date: DS.attr('date', {
  //   attrs: {
  //     time: true
  //   },
  //   label: 'Depart at'
  // }),
  // return_date: DS.attr('date', {
  //   attrs: {
  //     time: true
  //   },
  //   label: 'Return at'
  // }),
  means_of_transport: DS.attr({'label': 'Means of Transport', 'choices': CHOICES.TRANSPORTATION}),
  accommodation_price: DS.attr(),
  transportation_price: DS.attr(),
  // transport_days_manual: DS.attr(),
  // overnights_num_manual: DS.attr(),
  meal: DS.attr({'label': 'Meals', 'choices': CHOICES.MEALS}),
  // accommodation_default_currency: DS.attr(),
  // accommodation_local_price: DS.attr(),
  // accommodation_local_currency: DS.attr(),
  // accommodation_payment_way: DS.attr(),
  // accommodation_payment_description: DS.attr(),
  // transportation_default_currency: DS.attr(),
  // transportation_payment_way: DS.attr(),
  // transportation_payment_description: DS.attr(),
  // transport_days_proposed: DS.attr(),
  // overnight_cost: DS.attr(),
  // compensation_level: DS.attr(),
  // same_day_return_task: DS.attr(),
  // get_compensation: DS.attr(),
  // compensation_days_manual: DS.attr()
});
