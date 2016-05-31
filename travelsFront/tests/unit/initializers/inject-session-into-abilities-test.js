import Ember from 'ember';
import InjectSessionIntoAbilitiesInitializer from 'travels-front/initializers/inject-session-into-abilities';
import { module, test } from 'qunit';

let application;

module('Unit | Initializer | inject session into abilities', {
  beforeEach() {
    Ember.run(function() {
      application = Ember.Application.create();
      application.deferReadiness();
    });
  }
});

// Replace this with your real tests.
test('it works', function(assert) {
  InjectSessionIntoAbilitiesInitializer.initialize(application);

  // you would normally confirm the results of the initializer here
  assert.ok(true);
});
