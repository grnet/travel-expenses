import DS from 'ember-data';

export default DS.Model.extend({
   	name: DS.attr(),
 	cost: DS.attr(),
    petition: DS.belongsTo('petition'),
    url: DS.attr()

});
