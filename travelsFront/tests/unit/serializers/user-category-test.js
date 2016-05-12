import { moduleForModel, test } from 'ember-qunit';

moduleForModel('user-category', 'Unit | Serializer | user category', {
  // Specify the other units that are required for this test.
  needs: ['serializer:user-category']
});

// Replace this with your real tests.
test('it serializes records', function(assert) {
  let record = this.subject();

  let serializedRecord = record.serialize();

  assert.ok(serializedRecord);
});
