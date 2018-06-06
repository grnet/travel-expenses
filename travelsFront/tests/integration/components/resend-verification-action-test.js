import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('resend-verification-action', 'Integration | Component | resend verification action', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{resend-verification-action}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#resend-verification-action}}
      template block text
    {{/resend-verification-action}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
