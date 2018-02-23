import Ember from 'ember';
import {field} from 'ember-gen';
import TravelInfo from 'travel/models/travel-info'
import {resourceMetaFrom} from 'ember-gen/lib/meta';

export default Ember.Component.extend({
  modelMeta: Ember.computed(function() {
    let meta = {
    fieldsets: [
      {
        fields: [
          field('departure_point', { required: true }),
          field('arrival_point', { required: true }),
          field('depart_date', {}),
          field('return_date', {}),
        ],
        layout: { flex: [50, 50, 50, 50] }
      },
    ]};
    let model = TravelInfo;
    return resourceMetaFrom(TravelInfo, meta, model, Ember.getOwner(this));
  }),

});
