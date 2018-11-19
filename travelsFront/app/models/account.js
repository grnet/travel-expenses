import DS from 'ember-data';
import validate from 'ember-gen/validate';

function samePassword({field, checkLen}) {
  return (key, value, old, changes, content) => {
    if (changes.password && value && value.length >= (checkLen || 3)) {
      if (value != changes.password) {
        return 'passwords.do.not.match'
      }
    }
    return true;
  }
};

export default DS.Model.extend({
  __api__: {
    ns: 'auth',
    path: 'register',

    serialize(hash, snapshot, serializer) {
      delete hash['password2'];
      return hash;
    }
  },

  username: DS.attr('string'),
  email: DS.attr('string'),
  password: DS.attr('string', { formAttrs: { type: 'password' }, validators: [validate.length({min: 6})] }),
  password2: DS.attr('string', { formAttrs: { type: 'password' }, validators: [validate.presence(true), samePassword({field: 'password', checkLen: 1})] }),
});
