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
  'accommodation_cost',
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

const petitionDatesFields = [
  {
    key: 'departure_point',
    attrs: [
      'depart_date',
    ]
  },
  {
    key: 'arrival_point',
    attrs: [
      'task_start_date',
      'task_end_date',
      'return_date',
    ]
  }
];

function serializePetitionDate(serializer, payload, key, attrs) {
  const cityURL = payload[key];
  if (!cityURL) { 
    return;
  }
  let timezoneID = cityURL.split('/').slice(-2)[0];
  let city = serializer.store.peekRecord('city', timezoneID);
  let timezone = city.data.timezone;

  for (let attr of attrs) {
    const dateFromServer = payload[attr];
    if (dateFromServer) {
      const date = moment.tz(dateFromServer, timezone);
      const dateRaw = moment(date).format().slice(0, -6);
      const dateLocal = moment(dateRaw).toDate();
      payload[attr] = moment(dateLocal).format();
    }
  }
}

function deserializePetitionDate(serializer, payload, key, attrs) {
  const cityURL = payload[key];
  if (!cityURL) {
    return;
  }
  let timezoneID = cityURL.split('/').slice(-2)[0];
  let city = serializer.store.peekRecord('city', timezoneID);
  let timezone = city.data.timezone;

  for (let attr of attrs) {
    const dateFromUI = payload[attr];
    if (dateFromUI) {
      const rawDate = moment(dateFromUI).format().slice(0, -6);
      const dateLocal = moment.tz(rawDate, timezone).format();
      const dateUTC = moment.utc(dateLocal).format();
      payload[attr] = dateUTC.slice(0, -4);
    }
  }
}

const normalizePetition = function(hash, serializer) {
  let travel_info = hash['travel_info'];
  if (travel_info.length) {
    travel_info = travel_info[0];
    for (let field of TRAVEL_INFO_FIELDS) {
      if (field in travel_info) {
        hash[field] = travel_info[field];
      }
    }
  }

  for (let o of petitionDatesFields) {
    serializePetitionDate(serializer, hash, o.key, o.attrs);
  }

  delete hash['travel_info'];
  return hash;
}

const serializePetition = function(json, snapshot, serializer) {
  for (let o of petitionDatesFields) {
    deserializePetitionDate(serializer, json, o.key, o.attrs);
  }

  let travel_info = {};
  for (let field of TRAVEL_INFO_FIELDS) {
    if (field in json) {
      travel_info[field] = json[field];
      delete json[field];
    }
    if (field === 'travel_files') {
      debugger;
    }
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

  json['travel_info'] = [];
  if (Object.keys(travel_info).length) {
    json['travel_info'].push(travel_info);
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

