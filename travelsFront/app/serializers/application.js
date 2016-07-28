import DRFSerializer from 'ember-django-adapter/serializers/drf';
import {apiFor, urlJoin} from 'travels-front/adapters/util';


export default DRFSerializer.extend({

  serializeBelongsTo(snapshot, json, rel) {
    let resp = this._super(snapshot, json, rel);
    let key = this.keyForRelationship(rel.key);
    let api = apiFor(rel.type, this.container);
    if (json[key]) {
      json[key] = api.relURL(json[key]);
    }
    return resp;
  },

  serializeHasMany(snapshot, json, rel) {
    let resp = this._super(snapshot, json, rel);
    let key = this.keyForRelationship(rel.key);
    let api = apiFor(rel.type, this.container);
    if (json[key]) {
      json[key] = json[key].map(function(id) {
        return api.relURL(id);
      })
    }
    return resp;
  },

  normalize(modelClass, resourceHash, prop) {
    let api = apiFor(modelClass, this.container);
    if (api.normalize) {
      resourceHash = api.normalize(resourceHash, this);
    }
    return this._super(modelClass, resourceHash, prop);
  },

  serialize(snapshot, options) {
    let api = apiFor(snapshot.modelName, this.container);
    let json = this._super(snapshot, options);
    if (api.serialize) {
       return api.serialize(json, snapshot, this);
    }
    return json;
  }
})
