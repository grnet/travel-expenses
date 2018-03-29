import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  // key used in apimas spec
  resourceName: 'users',
  // related ember-data model
  modelName: 'user',

  // require authenticated user
  auth: true,
  menu: {
    display: true,
  },
});

