import Ember from 'ember';

export default Ember.Component.extend({
  i18n: Ember.inject.service(),
  classNames: ['language-select'],

  locales: Ember.computed('i18n.locale', 'i18n.locales', function() {
    const i18n = this.get('i18n');
    return this.get('i18n.locales').map(function (loc) {
      return { id: loc, text: i18n.t('language-select.language.' + loc) };
    });
  }),

  actions: {
    setLocale(loc) {
      this.set('i18n.locale', loc);
    }
  }
});
