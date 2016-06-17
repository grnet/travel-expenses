/* jshint node: true */
var API = 'http://127.0.0.1:8000';
module.exports = function(environment) {
	var ENV = {
		modulePrefix: 'travels-front',
		environment: environment,
		baseURL: '/',
		locationType: 'auto',
		EmberENV: {
			FEATURES: {
				// Here you can enable experimental features on an ember canary build
				// e.g. 'with-controller': true
			}
		},

		APP: {
			// Here you can pass flags/options to your application instance
			// when it is created 
			backend_host: API,
		},

		petition_status_1: API+'/petition/petition_status/1/',
		petition_status_2: API+'/petition/petition_status/2/',
		petition_status_3: API+'/petition/petition_status/3/',
		petition_status_4: API+'/petition/petition_status/4/',


	};

	ENV['ember-simple-auth'] = {
		authorizer: 'authorizer:token'
	};

	ENV['ember-simple-auth-token'] = {
		serverTokenEndpoint: ENV.APP.backend_host+'/auth/login/',
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
