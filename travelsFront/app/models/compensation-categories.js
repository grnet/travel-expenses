import DS from 'ember-data';

export default DS.Model.extend({
   	name: DS.attr(),
 	country_category: DS.belongsTo('country-category'),
    user_category: DS.belongsTo('category'),
    compensation: DS.attr(),
    url: DS.attr()

});
