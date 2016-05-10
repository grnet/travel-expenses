import { moduleForModel, test } from 'ember-qunit';

moduleForModel('country', 'Unit | Serializer | country', {
  // Specify the other units that are required for this test.
  needs: ['serializer:country']
});

// Replace this with your real tests.
test('it serializes records', function(assert) {
  let record = this.subject();

  let serializedRecord = record.serialize();

  assert.ok(serializedRecord);
});
