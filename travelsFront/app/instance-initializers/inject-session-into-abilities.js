export function initialize(/* application */) {
  // application.inject('route', 'foo', 'service:foo');
}

export default {
  name: 'inject-session-into-abilities',
  initialize(app) {
    app.inject('ability', 'session', 'session:main');
  }
};

