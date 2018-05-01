import Adapter from './application';

export default Adapter.extend({

  // Hacky way to handle the case when a PUT call to an application-item
  // returns a new id. The adapter is tricked into serializing the record
  // with the old id while keeping the new id as a model property.
  updateRecord(store, type, snapshot) {
    let old_id = snapshot.id;
    return this._super(store, type, snapshot).then(function(hash){
      let new_id = hash.id;
      if (new_id != old_id) {
        hash.new_id = new_id;
        hash.id = old_id;
      }
      return hash;
    });
  }
});
