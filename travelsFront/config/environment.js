/* jshint node: true */
var API_EP = 'http://localhost:8000/api';
var APPLICATION_URL_PREFIX='/app/';
var choices = require('../../resources/common');


module.exports = function(environment) {
	var ENV = {
		modulePrefix: 'travels-front',
		environment: environment,
		baseURL: '/ui/',
		locationType: 'auto',
		default_city: "1245",
    default_currency: "EUR",
    i18n : {
        defaultLocale: 'gr'
    },
		EmberENV: {
			FEATURES: {
				// Here you can enable experimental features on an ember canary build
				// e.g. 'with-controller': true
			}
		},

		APP: {
			backend_host: API_EP,
      resource_choices: choices,
		},

		petition_status_1: API_EP+'/petition/petition-status/1/',
		petition_status_2: API_EP+'/petition/petition-status/2/',
		petition_status_3: API_EP+'/petition/petition-status/3/',
		petition_status_4: API_EP+'/petition/petition-status/4/',


	};

  ENV.contentSecurityPolicy = {
    'default-src': "'none'",
    'script-src': "'self'",
    'font-src': "'self' http://fonts.gstatic.com",
    'connect-src': "'self'",
    'img-src': "'self' data:",
    'media-src': "'self'"
  };

	ENV['ember-simple-auth'] = {
		authorizer: 'authorizer:token'
	};

	ENV['ember-simple-auth-token'] = {
		serverTokenEndpoint: ENV.APP.backend_host + '/auth/login/',
		identificationField: 'username',
		passwordField: 'password',
		tokenPropertyName: 'auth_token',
		authorizationPrefix: 'Token ',
		authorizationHeaderName: 'Authorization',
		headers: {},
	};

	if (environment === 'development') {
		ENV['ember-cli-mirage'] = {
			enabled: false
		}
		// ENV.APP.LOG_RESOLVER = true;
		// ENV.APP.LOG_ACTIVE_GENERATION = true;
		// ENV.APP.LOG_TRANSITIONS = true;
		// ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
		// ENV.APP.LOG_VIEW_LOOKUPS = true;
	}

	if (environment === 'test') {
		// Testem prefers this...
		ENV.baseURL = '/';
		ENV.locationType = 'none';

		// keep test console output quieter
		ENV.APP.LOG_ACTIVE_GENERATION = false;
		ENV.APP.LOG_VIEW_LOOKUPS = false;

		ENV.APP.rootElement = '#ember-testing';
	}

	if (environment === 'production') {
		ENV['ember-cli-mirage'] = {
			enabled: true
		}
	}

	return ENV;
};
