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

const DATE_PARAMS = [
  'departure_point',
  'arrival_point',
  'task_start_date',
  'task_end_date',
  'depart_date',
  'return_date'
];

let FILE_FIELDS = [
  'travel_files'
]

const normalizePetition = function(hash, serializer) {
  let travel_info = hash['travel_info'];
  if (travel_info.length) {
    travel_info = travel_info[0];
    for (let field of TRAVEL_INFO_FIELDS) {
      if (field in travel_info) {
        hash[field] = travel_info[field];
      }
    }
  };
  //deserialize dates
  for (let key of DATE_PARAMS) {
    if (key == "departure_point") {
      let departureTimezoneID = hash[key].split('/').slice(-2)[0];
      let city = serializer.store.peekRecord('city', departureTimezoneID);
      let departureTimezone = city.data.timezone;
      //transform depart_date property
      let departDateFromServer = hash['depart_date'];
      let departDate = moment.tz(departDateFromServer, departureTimezone);
      let rawDepartDate = moment(departDate).format().slice(0, -6);
      let departDateLocal = moment(rawDepartDate).toDate();
      hash['depart_date'] = moment(departDateLocal).format();
    }
    else if (key == "arrival_point") {
      let arrivalTimezoneID = hash[key].split('/').slice(-2)[0];
      let city = serializer.store.peekRecord('city', arrivalTimezoneID);
      let arrivalTimezone = city.get('timezone');

      for (let attr of ['task_start_date', 'task_end_date', 'return_date']) {
        let dateFromServer = hash[attr];
        let date = moment.tz(dateFromServer, arrivalTimezone);
        let rawDate = moment(date).format().slice(0, -6);
        let dateLocal = moment(rawDate).toDate();
        hash[attr] = moment(dateLocal).format();
      }
    }
  };

  delete hash['travel_info'];
  return hash;
}

const serializePetition = function(json, snapshot, serializer) {
  //serialize dates
  for (let key of DATE_PARAMS) {
    if (key == "departure_point") {
      let departureTimezoneID = json[key].split('/').slice(-2)[0];
      let city = serializer.store.peekRecord('city', departureTimezoneID);
      let departureTimezone = city.data.timezone;
      //transform depart_date property
      let departDate = json['depart_date'];
      let rawDepartDate = moment(departDate).format().slice(0, -6);
      let departDateLocal = moment.tz(rawDepartDate, departureTimezone).format();
      let departDateUTC = moment.utc(departDateLocal).format();
      json['depart_date'] = departDateUTC.slice(0, -4);
    }
    else if (key == "arrival_point") {
      let arrivalTimezoneID = json[key].split('/').slice(-2)[0];
      let city = serializer.store.peekRecord('city', arrivalTimezoneID);
      let arrivalTimezone = city.get('timezone');

      for (let attr of ['task_start_date', 'task_end_date', 'return_date']) {
        let dateFromUi = json[attr];
        let rawDate = moment(dateFromUi).format().slice(0, -6);
        let dateLocal = moment.tz(rawDate, arrivalTimezone).format();
        let dateUTC = moment.utc(dateLocal).format();
        json[attr] = dateUTC.slice(0, -4);
      }
    }
  };

  let travel_info = {};
  for (let field of TRAVEL_INFO_FIELDS) {
    if (field in json) {
      travel_info[field] = json[field];
      delete json[field];
    }
    if (field === 'travel_files') {
      debugger;
    }
  };
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

