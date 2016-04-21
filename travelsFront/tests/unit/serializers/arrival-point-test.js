import { moduleForModel, test } from 'ember-qunit';

moduleForModel('arrival-point', 'Unit | Serializer | arrival point', {
  // Specify the other units that are required for this test.
  needs: ['serializer:arrival-point']
});

// Replace this with your real tests.
test('it serializes records', function(assert) {
  let record = this.subject();

  let serializedRecord = record.serialize();

  assert.ok(serializedRecord);
});
