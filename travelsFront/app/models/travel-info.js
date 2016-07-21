import DS from 'ember-data';

export default DS.Model.extend({
  url: DS.attr(),
	depart_date: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
  }),
	return_date: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
  }),
  departure_point: DS.belongsTo('city'),
  arrival_point: DS.belongsTo('city'),
  transportation: DS.attr(),
  accomondation_price: DS.attr(),
  transportation_price: DS.attr(),
  transport_days_manual: DS.attr(),
  overnights_num_manual: DS.attr(),
  meals: DS.attr(),
  movement_num: DS.attr()
});
