// export function initialize(/* appInstance */) {
//   // appInstance.inject('route', 'foo', 'service:foo');
// }

export function initialize(appInstance) {
  const service = Ember.ObjectProxy.create({ isServiceFactory: true });
  appInstance.register('service:current-user', service, { instantiate: false, singleton: true });
  appInstance.inject('route', 'currentUser', 'service:current-user');
  appInstance.inject('controller', 'currentUser', 'service:current-user');
  appInstance.inject('component', 'currentUser', 'service:current-user');
  appInstance.inject('serializer', 'currentUser', 'service:current-user');
}

export default {
  name: 'current-user',
  initialize: initialize

};
