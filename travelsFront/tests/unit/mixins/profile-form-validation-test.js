import Ember from 'ember';
import ProfileFormValidationMixin from 'travels-front/mixins/profile-form-validation';
import { module, test } from 'qunit';

module('Unit | Mixin | profile form validation');

// Replace this with your real tests.
test('it works', function(assert) {
  let ProfileFormValidationObject = Ember.Object.extend(ProfileFormValidationMixin);
  let subject = ProfileFormValidationObject.create();
  assert.ok(subject);
});
