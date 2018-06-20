import Ember from 'ember';
import gen from 'ember-gen/lib/gen';

const {
  get,
  computed,
  computed: { reads },
} = Ember;

let contact = gen.GenRoutedObject.extend({
  auth: null,
  name: 'contact',
  resourceName: '',
  templateName: 'contact',
  path: "contact",
  menu: {
    order: 400,
    display: true,
    icon: 'mail',
    label: 'contact.tab',
  },
});

export default gen.GenRoutedObject.extend({
  name: 'contact',
  gens: { contact }
})
