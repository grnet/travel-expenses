import DS from 'ember-data';
import _ from 'lodash/lodash';


const { get } = Ember;

const idFromUrl = function(url) {
  let parts = url.split("/").filter((v) => v);
  return parts[parts.length - 1];
};

const CACHE = {};
const TIMEOUT = 10 * 1000; // 10 seconds


export default DS.Store.extend({

  findAll(model) {
    let cacheKey = `findAll${model}`;
    let cacheMatch = CACHE[`findAll${model}`];
    let now = (new Date()).getTime();

    if (cacheMatch !== undefined && (cacheMatch[1] + TIMEOUT) >= now) {
      console.log(`Cache match found for key ${cacheKey}`);
      return cacheMatch[0];
    }
    let resp = this._super(...arguments);
    CACHE[cacheKey] = [resp, (new Date()).getTime()];
    return resp;
  },

  findBelongsTo: function(owner, link, relationship) {
    let record = owner.record;
    let ref = record.belongsTo(relationship.key);
    let id = ref.id() || idFromUrl(ref.link());
    let type = relationship.type;
    let cacheKey = `${type}:${id}`;
    let now = (new Date()).getTime();
    let cacheMatch = CACHE[cacheKey];

    if (cacheMatch === undefined) {
      let peeked = this.peekRecord(type, id);
      if (peeked) {
        cacheMatch = CACHE[cacheKey] = [peeked._internalModel, (new Date()).getTime()];
      }
    }

    if (cacheMatch && (cacheMatch[1] + TIMEOUT) >= now) {
      return new Ember.RSVP.Promise((r) => { r(cacheMatch[0]) });
    }

    return this._super(...arguments).then((resp) => {
      CACHE[cacheKey] = [resp, (new Date()).getTime()];
      return resp;
    });
  },

  _eachEmbeddedRelationship(internalModel, callback) {
    return internalModel.eachRelationship((key, rel) => {
      if (rel.kind == 'hasMany' && rel.options && rel.options.embedded) {
        callback(key, rel);
      }
    });
  },

  didSaveRecord(internalModel, dataArg) {
    this._super(internalModel, dataArg);
    let record = internalModel.getRecord();
    this._eachEmbeddedRelationship(internalModel, (key, rel) => {
      let rels = get(record, key);
      rels.forEach(model => { 
        model._internalModel.clearErrorMessages();
      });
    });
  },

  recordWasInvalid(internalModel, errors) {
    let record = internalModel.getRecord();
    // propagate hasMany errors
    this._eachEmbeddedRelationship(internalModel, (key, rel) => {
      if (key in errors) {
        let rels = get(record, key);

        for (let index = 0; index < errors[key].length; index++) {
          let obj = rels.objectAt(index);
          for (let attr in errors[key][index]) {
            obj._internalModel.addErrorMessageToAttribute(attr, errors[key][index][attr]);
          }
        }
      }
    });
    return this._super(internalModel, errors);
  }
})
