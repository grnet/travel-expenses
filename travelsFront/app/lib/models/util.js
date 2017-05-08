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
      //transform task_start_date property
      let taskStartDateFromServer = hash['task_start_date'];
      let taskStartDate = moment.tz(taskStartDateFromServer, arrivalTimezone);
      let rawTaskStartDate = moment(taskStartDate).format().slice(0, -6);
      let taskStartDateLocal = moment(rawTaskStartDate).toDate();
      hash['task_start_date'] = moment(taskStartDateLocal).format();
      //transform task_end_date property
      let taskEndDateFromServer = hash['task_end_date'];
      let taskEndDate = moment.tz(taskEndDateFromServer, arrivalTimezone);
      let rawTaskEndDate = moment(taskEndDate).format().slice(0, -6);
      let taskEndDateLocal = moment(rawTaskEndDate).toDate();
      hash['task_end_date'] = moment(taskEndDateLocal).format();
      //transform return_date property
      let returnDateFromServer = hash['return_date'];
      let returnDate = moment.tz(returnDateFromServer, arrivalTimezone);
      let rawReturnDate = moment(returnDate).format().slice(0, -6);
      let returnDateLocal = moment(rawReturnDate).toDate();
      hash['return_date'] = moment(returnDateLocal).format();
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
      //transform task_start_date property
      let taskStartDate = json['task_start_date'];
      let rawTaskStartDate = moment(taskStartDate).format().slice(0, -6);
      let taskStartDateLocal = moment.tz(rawTaskStartDate, arrivalTimezone).format();
      let taskStartDateUTC = moment.utc(taskStartDateLocal).format();
      json['task_start_date'] = taskStartDateUTC.slice(0, -4);
      //transform task_end_date property
      let taskEndDate = json['task_end_date'];
      let rawTaskEndDate = moment(taskEndDate).format().slice(0, -6);
      let taskEndDateLocal = moment.tz(rawTaskEndDate, arrivalTimezone).format();
      let taskEndDateUTC = moment.utc(taskEndDateLocal).format();
      json['task_end_date'] = taskEndDateUTC.slice(0, -4);
      //transform return_date property
      let returnDate = json['return_date'];
      let rawReturnDate = moment(returnDate).format().slice(0, -6);
      let returnDateLocal = moment.tz(rawReturnDate, arrivalTimezone).format();
      let returnDateUTC = moment.utc(returnDateLocal).format();
      json['return_date'] = returnDateUTC.slice(0, -4);
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

