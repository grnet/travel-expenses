import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    ns: 'auth',
    path: 'register',
  },

  username: DS.attr('string'),
  password: DS.attr('string', { formAttrs: { type: 'password' } }),
  email: DS.attr('string'),
});
