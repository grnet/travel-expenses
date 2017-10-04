/* jshint node: true */
var choices = require('../../resources/common');

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'travel',
    environment: environment,
    rootURL: '/ui/',
    appURL: '/api/',
    locationType: 'auto',
    i18n : {
      defaultLocale: 'gr'
    },
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },
    APP: {}
  };

  ENV['ember-simple-auth'] = {
    authenticationRoute: 'auth.index',
    authorizer: 'authorizer:token'
  };

  ENV['ember-simple-auth-token'] = {
    serverTokenEndpoint: '/api/auth/login/',
    identificationField: 'username',
    passwordField: 'password',
    tokenPropertyName: 'auth_token',
    authorizationPrefix: 'Token ',
    authorizationHeaderName: 'Authorization',
    headers: {},
  };

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  return ENV;
};
