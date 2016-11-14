import Ember from 'ember';
import Resolver from './resolver';
import DS from 'ember-data';
import loadInitializers from 'ember-load-initializers';
import config from './config/environment';

let App;

Ember.MODEL_FACTORY_INJECTIONS = true;

export default DS.DateTransform.reopen({

	deserialize(serialized) {
    var type = typeof serialized;

    if (type === "string") {
      return new Date(moment(serialized).format("YYYY-MM-DDTHH:mmZ"));
    } else if (type === "number") {
      return new Date(serialized);
    } else if (serialized === null || serialized === undefined) {
      // if the value is null return null
      // if the value is not present in the data return undefined
      return serialized;
    } else {
      return null;
    }
	},

	serialize(date) {
		if (date instanceof Date && !isNaN(date)) {
      return moment(date).format("YYYY-MM-DDTHH:mm");
    } else {
      return null;
		}
	}
});

App = Ember.Application.extend({
  modulePrefix: config.modulePrefix,
  podModulePrefix: config.podModulePrefix,
  Resolver
});

loadInitializers(App, config.modulePrefix);

export default App;
