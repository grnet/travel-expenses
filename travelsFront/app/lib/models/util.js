import Ember from 'ember';

const {
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
  delete hash['travel_info'];
  return hash;
}

const serializePetition = function(json) {
  let travel_info = {};
  for (let field of TRAVEL_INFO_FIELDS) {
    if (field in json) {
      travel_info[field] = json[field];
      delete json[field];
    }
  }
  json['travel_info'] = [];
  if (Object.keys(travel_info).length) {
    json['travel_info'].push(travel_info);
  }
  return json;
}

const preloadPetitions = function(petitionModel, store) {
  return new Ember.RSVP.Promise((resolve, reject) => {
    store.findAll('city').then(() => {
      store.findAll('project').then(() => {
        if (!isArray(petitionModel)) {
          petitionModel = [petitionModel];
        }
        let petitions = Promise.all(petitionModel.map((m) => { return store.query(m, {})}));
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
  model() {
    return preloadPetitions(get(this, 'petitionModel'), get(this, 'store'));
  }
});
export {normalizePetition, serializePetition, PetitionListRoute, preloadPetitions}
