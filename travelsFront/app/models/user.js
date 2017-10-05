import DS from 'ember-data';

const SIGNUP_UI = {}

export default DS.Model.extend({
  __api__: {
    ns: 'auth',
    path: 'register'
  },
  __ui__: {
    'signup': SIGNUP_UI,
  },
  username: DS.attr('string'),
  password: DS.attr('string', {formAttrs: {type: 'password'}}),
  email: DS.attr('string')
});
