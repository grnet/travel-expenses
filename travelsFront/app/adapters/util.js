import Ember from 'ember';
import _ from 'lodash/lodash';
import ENV from 'travels-front/config/environment'; 

const { getOwner, assert } = Ember;

const urlJoin = function(...args) {
  let parts = []
  args.forEach((p) => {
    if (Ember.isArray(p)) {
      parts = parts.concat(urlJoin.apply(this, p));
      return;
    } else {
      parts = parts.concat((p || '').toString().split("/").map(
        (k) => k && k.toString().trim()
      ).map(
        (k) => k.replace(/\/\//g, "").replace(/:$/, ":\/")
      ).filter((k) => k))
    }
  });
  return parts.join("/");
}

const ApiParams = Ember.Object.extend({
  apiBase: ENV.APP.backend_host,
  urlJoin: urlJoin,

  pathForType(adapter, type) {
    return urlJoin(this.ns, this.path || type)
  },

  buildURL(adapter, url, id, snapshot, requestType, query) {
    return url;
  },

  relURL(id) {
    return urlJoin(this.apiBase, this.ns, this.path, this.type.modelName, id) + '/';
  }
});

const apiFor = function(modelOrType, subject) {
  let container = getOwner(subject);
  assert("Cannot resolve container of " + subject.toString(), container);
  container = container.__container__;

  let type = modelOrType;
  if (typeof modelOrType === "string") {
    type = container.lookupFactory(`model:${modelOrType}`);
  };
  let ext = type.prototype.__api__ || {};
  return ApiParams.extend(ext).create({container: container, type:type});
};


export {apiFor, urlJoin};
