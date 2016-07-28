import {Petition} from 'travels-front/lib/models/petition';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';


var Validations = buildValidations({
    iban: validator('iban-validator'),
});


const TRAVEL_INFO_FIELDS = ['departure_point', 'arrival_point'];

export default Petition.extend(Validations, {
  __api__: {
    path: 'petition/user/saved/',

    normalize: function(hash, serializer) {
      let travel_info = hash['travel_info'];
      if (travel_info.length) {
        travel_info = travel_info[0];
        for (let field of TRAVEL_INFO_FIELDS) {
          if (travel_info[field]) {
            hash[field] = travel_info[field];
          }
        }
      }
      delete hash['travel_info'];
      return hash;
    },

    serialize: function(json) {
      let travel_info = {};
      for (let field of TRAVEL_INFO_FIELDS) {
        if (json[field]) {
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
  },
  __ui__: {
   'default': UIS['petition_user'],
  } 
});
