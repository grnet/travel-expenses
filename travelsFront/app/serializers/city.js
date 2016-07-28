import Base from './application';
import DS from 'ember-data';

export default Base.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    country: { embedded: 'always' }
  }
})
