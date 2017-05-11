import DS from 'ember-data';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';
import DRFAdapter from 'ember-django-adapter/adapters/drf';
import ENV from 'travels-front/config/environment'; 
import {apiFor, urlJoin} from 'travels-front/adapters/util';


export default DRFAdapter.extend(DataAdapterMixin, {
  
	host: ENV.APP.backend_host,
	contentType: 'application/json',
	dataType: 'json',
	authorizer: 'authorizer:token',
  disableRoot: true,

  pathForType: function(type) {
    return apiFor(type, this).pathForType(this, type);
  },

	buildURL: function(modelName, id, snapshot, requestType, query) {
		var url = this._super(modelName, id, snapshot, requestType, query);
    return apiFor(modelName, this).buildURL(this, url, id, snapshot, requestType, query);
	},

  urlForModel: function(model) {
    let name = model.constructor.modelName;
    let id = model.get('id');
    return this.buildURL(name, id, {}, 'findRecord');
  },

  action: function(model, action, method='POST') {
    let actionURL = this.urlForModel(model) + action + '/';
    return this.ajax(actionURL, method);
  },

  objectToFormData: function(obj) {
    var fd = new FormData();
    var formKey;
    for (var property in obj) {
      if (obj.hasOwnProperty(property)) {
        formKey = property;
        if (typeof obj[property] === 'object' && !(obj[property] instanceof File)) {
          // django mimeparser does not support array values declared as []
          fd.append(formKey, JSON.stringify(obj[property]));
        } else {
          fd.append(formKey, obj[property]);
        }
      }
    };
    return fd;
  },
    
  _getFormData: function(data) {
    let formData = this.objectToFormData(data);
    return formData;
  },

  patchRecord(store, type, snapshot) {
    let data = {};
    let serializer = store.serializerFor(type.modelName);

    serializer.serializeIntoHash(data, type, snapshot, {patch: true});
    let changed = Object.keys(snapshot.changedAttributes());
    Object.keys(data).forEach((key) => {
      if (!changed.includes(key)) {
        delete data[key];
      }
    });

    let id = snapshot.id;
    let url = this.buildURL(type.modelName, id, snapshot, 'updateRecord');
    return this.ajax(url, "PATCH", { data: data });
  },

  // Overwrite to change the request types on which Form Data is sent
  formDataTypes: ['POST', 'PUT', 'PATCH'],

  // Overwrite to flatten the form data by removing the root
  disableRoot: false,

  ajaxOptions: function(url, type, options) {
    let data = {};

    if (options && 'data' in options) { data = options.data; }

    let hash = this._super.apply(this, arguments);
    let files = Object.keys(data).filter((key) => {
      return data[key] instanceof window.File;
    });

    if (typeof FormData !== 'undefined' && data && this.formDataTypes.indexOf(type) >= 0 && files.length) {
      hash.processData = false;
      hash.contentType = false;
      hash.data = this._getFormData(data);
    }
    return hash;
  },

  findRecord(store, type, id, snapshot) {
    // custom logic just for petition models
    if (!type || !type.modelName || (type.modelName.indexOf('petition') === -1 && type.modelName.indexOf('compensation') === -1)) {
      return this._super(store, type, id, snapshot);
    }

    // Try to preload cities prior to resolving petition payload data.
    // Cities timezones are injected to payload making them accessible
    // in petition record normalize methods.
    return this._super(store, type, id, snapshot).then((payload) => {
      const points = ['departure_point', 'arrival_point'];
      const travel_info_props = payload.travel_info[0];

      const timezonePromises = points.map(point => {
        const cityURL = travel_info_props[point];
        if (!cityURL) {
          /* return null if no cityURL exists */
          return Ember.RSVP.resolve(null);
        }

        const cityId = cityURL.split('/').slice(-2)[0];
        const record = store.peekRecord('city', cityId);
        return record
          ? Ember.RSVP.resolve(record.get('timezone'))
          : store.findRecord('city', cityId).then(city => city.get('timezone'));
      });

      return Ember.RSVP.all(timezonePromises).then(records => {
        for (var i = 0; i < points.length; ++i) {
          const point = points[i];
          const record = records[i];
          payload[`${point}_timezone`] = record;
        }
        return payload;
      });
    });
  },
});
