import Ember from 'ember';
import TravelInfo from 'travel/models/travel-info';
import { resourceMetaFrom } from 'ember-gen/lib/meta';
import TRAVEL_INFO from '../utils/application/travel-info';

export default Ember.Component.extend({
  modelMeta: Ember.computed(function() {
    let meta = {
      fieldsets: Ember.computed(function() {
        let session = this.container.lookup('service:session');
        let role = session.get('session.authenticated.user_group');
        let res = [];

        if (role === 'USER' || role === 'MANAGER') {
          res = TRAVEL_INFO.FS_VIEW_1_USER;
        } else if (role === 'SECRETARY') {
          res = TRAVEL_INFO.FS_VIEW_3_SECRETARY;
        } else if (role === 'CONTROLLER') {
          res = TRAVEL_INFO.FS_VIEW_8_CONTROLLER;
        }

        return res;
      }) };
    let model = TravelInfo;

    return resourceMetaFrom(TravelInfo, meta, model, Ember.getOwner(this));
  }),

});
