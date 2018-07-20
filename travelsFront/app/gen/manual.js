import Ember from 'ember';
import gen from 'ember-gen/lib/gen';

const {
  get,
  inject,
  computed,
  computed: { reads },
} = Ember;

let manual = gen.GenRoutedObject.extend({
  auth: true,
  name: 'manual',
  resourceName: '',
  templateName: 'manual',
  path: 'manual',
  menu: {
    order: 600,
    display: true,
    icon: 'help',
    label: 'help.tab',
  },
});

export default gen.GenRoutedObject.extend({
  name: 'manual',
  gens: { manual }
})
