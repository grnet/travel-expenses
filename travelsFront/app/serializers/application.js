import DRFSerializer from 'ember-django-adapter/serializers/drf';
import {apiFor, urlJoin} from 'travels-front/adapters/util';


export default DRFSerializer.extend({

  serializeBelongsTo(snapshot, json, rel) {
    let resp = this._super(snapshot, json, rel);
    let key = this.keyForRelationship(rel.key);
    let api = apiFor(rel.type, this);
    if (json[key]) {
      json[key] = api.relURL(json[key]);
    }
    return resp;
  },


  extractErrors(store, typeClass, payload, id) {
    let api = apiFor(typeClass, this);
    if (api.normalizeErrors && payload && payload.errors) {
      payload.errors = api.normalizeErrors(payload.errors, this);
    }
    return this._super(store, typeClass, payload, id);
  },

  serializeHasMany(snapshot, json, rel) {
    let resp = this._super(snapshot, json, rel);
    let key = this.keyForRelationship(rel.key);
    let api = apiFor(rel.type, this);
    if (json[key]) {
      json[key] = json[key].map(function(id) {
        return api.relURL(id);
      })
    }
    return resp;
  },

  normalize(modelClass, resourceHash, prop) {
    let api = apiFor(modelClass, this);
    if (api.normalize) {
      resourceHash = api.normalize(resourceHash, this);
    }
    return this._super(modelClass, resourceHash, prop);
  },

  serialize(snapshot, options) {
    let api = apiFor(snapshot.modelName, this);
    let json = this._super(snapshot, options);
    if (api.serialize) {
       return api.serialize(json, snapshot, this);
    }
    return json;
  },

  /**
   * Inject hasMany urls to id coercion here in order for relationships to
   * get setup as expected.
   */
  extractRelationships(modelClass, resourceHash) {
    modelClass.eachRelationship((key, relationshipMeta) => {
      if (relationshipMeta.kind === 'hasMany') {
        let ids = (resourceHash[key] || []).map((url) => {
          // TODO: place this as a util method (idFromURL)
          return url.split('/').filter(Boolean).slice(-1)[0];
        });
        resourceHash[key] = ids;
      }
    });
    return this._super(modelClass, resourceHash);
  },
})
