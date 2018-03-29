import DS from 'ember-data';
import Serializer from './application';

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: { 'travel_info': { embedded: 'always' } },
})
