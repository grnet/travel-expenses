import Serializer from './application';
import DS from 'ember-data';

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: { 'travel_info': { embedded: 'always' } },
})
