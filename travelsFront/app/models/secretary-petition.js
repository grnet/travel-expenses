import {SecretaryPetition} from 'travels-front/lib/models/petition';
import {validator, buildValidations} from 'ember-cp-validations';


var Validations = buildValidations({
    iban: validator('iban-validator'),
});


export default Petition.extend(Validations, {
  __api__: {
    path: 'petition/secretary/saved/',
    buildURL: function(adapter, url, id, snap, rtype, query) {
      // always return my profile endpoint
      return this.urlJoin(adapter.get('host'), this.ns, this.path) + '/';
    }
  },
});
