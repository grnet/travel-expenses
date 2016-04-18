import { moduleFor, test } from 'ember-qunit';

moduleFor('validator:afm-validator', 'Unit | Validator | afm-validator', {
  needs: ['validator:messages']
});

test('it works', function(assert) {
  var validator = this.subject();
  assert.ok(validator);
});
