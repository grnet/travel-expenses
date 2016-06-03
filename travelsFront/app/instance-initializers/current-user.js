export function initialize(appInstance) {

  	appInstance.inject('route', 'account', 'service:account');
  	appInstance.inject('controller', 'account', 'service:account');
  	appInstance.inject('template', 'account', 'service:account');
}

export default {
	name: 'account',
	initialize: initialize
};
