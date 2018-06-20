import Ember from 'ember';
import gen from 'ember-gen/lib/gen';

const {
  get,
  computed,
  computed: { reads },
} = Ember;

let guidelines = gen.GenRoutedObject.extend({
  auth: null,
  name: 'guideline',
  resourceName: '',
  templateName: 'guideline',
  path: "guidelines",
  menu: {
    order: 300,
    display: true,
    icon: 'help',
    label: 'help.tab',
  },
});

export default gen.GenRoutedObject.extend({
  name: 'help',
  gens: { guidelines }
})
