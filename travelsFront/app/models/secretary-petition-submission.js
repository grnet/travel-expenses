import {SecretaryPetition} from 'travels-front/lib/models/secretary-petition';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';
import {normalizePetition, serializePetition} from 'travels-front/lib/models/util';

var Validations=buildValidations({
  first_name: [
    validator('presence', true),
  ],
  taskstartdate: [
    validator('presence', true),
  ],
});


export default SecretaryPetition.extend(Validations, {
  __api__: {
    path: 'petition-secretary-submitted/',
    normalize: normalizePetition, 
    serialize: serializePetition
  },
  __ui__: {
   'default': UIS['petition_travel'],
  },

  // cancel: function() {
  //   let adapter = this.store.adapterFor('secretary-petition-submission');
  //   return adapter.action(this, 'cancel');
  // }

});

