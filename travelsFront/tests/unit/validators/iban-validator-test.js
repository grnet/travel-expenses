import { moduleFor, test } from 'ember-qunit';

moduleFor('validator:iban-validator', 'Unit | Validator | iban-validator', {
  needs: ['validator:messages']
});

test('it works', function(assert) {
  var validator = this.subject();
  assert.ok(validator);
});
