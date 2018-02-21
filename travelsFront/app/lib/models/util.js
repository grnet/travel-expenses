import Ember from 'ember';

const {
  set,
  get,
  isArray,
  RSVP: { Promise }
} = Ember;

const TRAVEL_INFO_FIELDS = [
  'departure_point',
  'arrival_point',
  'depart_date',
  'return_date',
  'meals',
  'means_of_transport',
  'transportation_cost',
  'accommodation_local_cost',
  'accommodation_local_currency',
  'transport_days_manual',
  'transport_days_proposed',
  'compensation_days_manual',
  'compensation_days_proposed', 
  'accommodation_total_cost',
  'accommodation_default_currency',
  'accommodation_payment_way',
  'accommodation_payment_description',
  'transportation_default_currency',
  'transportation_payment_way',
  'transportation_payment_description',
  'overnights_num_manual',
  'overnight_cost',
  'compensation_level',
  'same_day_return_task',
];

let FILE_FIELDS = [
  'travel_files'
];

const petitionDateFields = [
  {
    key: 'travel_info.${i}.departure_point',
    attrs: [
      'travel_info.${i}.depart_date',
    ]
  },
  {
    key: 'travel_info.${i}.arrival_point',
    attrs: [
      'travel_info.${i}.return_date',
    ]
  },
  {
    key: 'travel_info.${first}.arrival_point',
    attrs: [
      'task_start_date',
    ]
  },
  {
    key: 'travel_info.${last}.arrival_point',
    attrs: [
      'task_end_date',
    ]
  }
];

function serializePetitionDate(serializer, payload, key, attrs) {
  const cityURL = get(payload, key);
  if (!cityURL) { 
    return;
  }
  const timezoneID = cityURL.split('/').slice(-2)[0];
  const city = serializer.store.peekRecord('city', timezoneID);
  const timezone = city.data.timezone;

  for (const attr of attrs) {
    const dateFromServer = get(payload, attr);
    if (dateFromServer) {
      const date = moment.tz(dateFromServer, timezone);
      if (date._offset == -0) {
        const dateRaw = moment(date).format().slice(0, -1);
        const dateLocal = moment(dateRaw).toDate();
        set(payload, attr, moment(dateLocal).format());
      } else {
        const dateRaw = moment(date).format().slice(0, -6);
        const dateLocal = moment(dateRaw).toDate();
        set(payload, attr, moment(dateLocal).format());
      }
    }
  }
}

function deserializePetitionDate(serializer, payload, key, attrs) {
  const cityURL = get(payload, key);
  if (!cityURL) {
    return;
  }
  const timezoneID = cityURL.split('/').slice(-2)[0];
  const city = serializer.store.peekRecord('city', timezoneID);
  const timezone = city.data.timezone;

  for (const attr of attrs) {
    const dateFromUI = get(payload, attr);
    if (dateFromUI) {
      const dateRaw = moment(dateFromUI).format().slice(0, -6);
      const dateLocal = moment.tz(dateRaw, timezone).format();
      const dateUTC = moment.utc(dateLocal).format();
      set(payload, attr, dateUTC.slice(0, -4));
    }
  }
}

function getDateKeys(hash) {
  let serializeKeys = [];

  for (let tzParams of petitionDateFields) {
    let _serializeKeys = [];
    let parts = tzParams.key.split('.');
    let key = [];

    parts.forEach((part, index) => {
      if (index == 0) { _serializeKeys.push([part]); return; }

      if (part == '${i}') {
        let expanded = [];
        _serializeKeys.forEach((key) => {
          get(hash, key.join('.')).forEach((_, i) => {
            expanded.push(key.concat([i]));
          });
        });
        _serializeKeys = expanded;
      } else if (part == '${last}') {
        _serializeKeys = _serializeKeys.map((key) => {
          let last = get(hash, key.join('.'));
          key.push(last.length - 1);
          return key;
        });
      } else if (part == '${first}') {
        _serializeKeys = _serializeKeys.map((key) => {
          key.push(0);
          return key;
        });
      } else {
        _serializeKeys = _serializeKeys.map((key) => {
          key.push(part);
          return key;
        });
      }
    });

    let _keys = []
    _serializeKeys = _serializeKeys.map((key) => {
      let _serializeKey = { tzField: key.join('.'), dateFields: [] };
      _keys.push(_serializeKey);

      tzParams.attrs.forEach((attr) => {
        let _attr = attr;
        if (attr.indexOf('${i}')) {
          _attr = _attr.split('.').map((part, i) => {
            if (part == '${i}') {
              return key[i];
            }
            return part;
          }).join('.');
        }
        _serializeKey.dateFields.push(_attr);
      });
    });
    serializeKeys = serializeKeys.concat(_keys);
  }
  return serializeKeys;
}

const normalizePetition = function(hash, serializer) {

  let serializeKeys = getDateKeys(hash);
  for (let key of serializeKeys) {
    serializePetitionDate(serializer, hash, key.tzField, key.dateFields);
  }

  if (hash.travel_info && hash.travel_info.length) {
    hash.travel_info.forEach((info, i) => {
      info.index = i + 1;
    });
  }
  return hash;
}

const serializePetition = function(json, snapshot, serializer) {
  let serializeKeys = getDateKeys(json);
  for (let key of serializeKeys) {
    deserializePetitionDate(serializer, json, key.tzField, key.dateFields);
  }

  // File fields values are set as
  //
  // - `File object` in case the user requested to upload a new file. we 
  //   keep the File object as value of the field payload. Adapter will 
  //   recognize file upload and do a FormData request.
  //
  // - `URL string` which means that user didn't request to change the field 
  //   and thus we remove the field from the json payload as server  
  //   reject string (non-file) values and retain the associated file
  //   
  // - `null` which should result the server to clear the value of the field
  //
  for (let field of FILE_FIELDS) {
    let val = json[field];
    if (val && typeof val === 'string') {
      delete json[field];
    }
    if (!val) { json[field] = null; }
  }
  return json;
}

const preloadPetitions = function(petitionModel, store, query) {
  query = query || {};
  return new Ember.RSVP.Promise((resolve, reject) => {
    store.findAll('city').then(() => {
      store.findAll('project').then(() => {
        if (!isArray(petitionModel)) {
          petitionModel = [petitionModel];
        }

        let petitions = Promise.all(petitionModel.map((m) => {return store.query(m, query)}));
        petitions.then((results) => {
          let model = results.reduce((prev, cur) => { return prev.concat(cur.toArray()); }, []);
          model.reload = function() {
            preloadPetitions(petitionModel, store).then(function(newModels) {
              model.setObjects(newModels);
            });
          }
          resolve(model);
        }, reject);

        petitions.then((p) => {
          resolve(petitions);
        }, reject);
      }, reject)
    }, reject);
  });
};

const PetitionListRoute = Ember.Route.extend({
  petitionModel: null,
  model(params) {
    return preloadPetitions(get(this, 'petitionModel'), get(this, 'store'));
  },
  setupController(controller, model){
    this._super(controller, model);
    controller.set('petitionModel', this.petitionModel);
  }
});
export {normalizePetition, serializePetition, PetitionListRoute, preloadPetitions}

