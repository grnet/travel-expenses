import gen from 'ember-gen/lib/gen';
import routes from 'ember-gen/lib/routes';

function resetHash(win, replace='') {
  if (win.history.replaceState) {
    win.history.replaceState(null, null, '#' + replace);
  } else {
    win.location.hash = replace;
  }
}

const Register = gen.GenRoutedObject.extend({
  auth: false,
  menu: {
    display: true,
    label: 'signup.tab',
    breadcrumb: { display: true },
  },
  modelName: 'account',
  routeBaseClass: routes.CreateRoute.extend(),
  component: 'gen-form',
  templateName: 'travel-register',
  onSubmit(model) {
    this.controllerFor('auth.register.index').set('registeredModel', model);
    this.transitionTo('auth.login.index');

    return false;
  },

  messages: {
    success: 'user.created',
  },
});

export { Register, resetHash };
