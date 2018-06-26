const {
  computed,
  get
} = Ember;

const STATUS_MAP = {
  'SAVED_BY_USER': 1,
  'SUBMITTED_BY_USER': 2,
  'SAVED_BY_SECRETARY': 3,
  'SUBMITTED_BY_SECRETARY': 4,
  'APPROVED_BY_PRESIDENT': 5,
  'USER_COMPENSATION': 6,
  'USER_COMPENSATION_SUBMISSION': 7,
  'SECRETARY_COMPENSATION': 8,
  'SECRETARY_COMPENSATION_SUBMISSION': 9,
  'PETITION_FINAL_APPOVAL': 10,
};

let abilityStates = {
  usersaved: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['SAVED_BY_USER'];
  }),
  ownedusersaved: computed('model.status', 'model.user_id', function() {
    let status = this.get('model.status');
    let userId = this.get('session.session.authenticated.id');
    let applicationUserId = this.get('model.user_id');
    return userId === applicationUserId && status === STATUS_MAP['SAVED_BY_USER'];
  }),
  usersubmitted: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['SUBMITTED_BY_USER'];
  }),
  ownedusersubmitted: computed('model.status', 'model.user_id', function() {
    let status = this.get('model.status');
    let userId = this.get('session.session.authenticated.id');
    let applicationUserId = this.get('model.user_id');

    return userId === applicationUserId && status === STATUS_MAP['SUBMITTED_BY_USER'];
  }),
  secretarysaved: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['SAVED_BY_SECRETARY'];
  }),
  secretarysubmitted: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['SUBMITTED_BY_SECRETARY'];
  }),
  presidentapproved: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['APPROVED_BY_PRESIDENT'];
  }),
  ownedpresidentapproved: computed('model.status', 'model.user_id', function() {
    let status = this.get('model.status');
    let userId = this.get('session.session.authenticated.id');
    let applicationUserId = this.get('model.user_id');

    return userId === applicationUserId && status === STATUS_MAP['APPROVED_BY_PRESIDENT'];
  }),
  usercompensationsaved: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['USER_COMPENSATION'];
  }),
  ownedusercompensationsaved: computed('model.status', 'model.user_id', function() {
    let status = this.get('model.status');
    let userId = this.get('session.session.authenticated.id');
    let applicationUserId = this.get('model.user_id');

    return userId === applicationUserId && status === STATUS_MAP['USER_COMPENSATION'];
  }),
  usercompensationsubmitted: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['USER_COMPENSATION_SUBMISSION'];
  }),
  ownedusercompensationsubmitted: computed('model.status', 'model.user_id', function() {
    let status = this.get('model.status');
    let userId = this.get('session.session.authenticated.id');
    let applicationUserId = this.get('model.user_id');

    return userId === applicationUserId && status === STATUS_MAP['USER_COMPENSATION_SUBMISSION'];
  }),
  secretarycompensationsaved: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['SECRETARY_COMPENSATION'];
  }),
  secretarycompensationsubmitted: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['SECRETARY_COMPENSATION_SUBMISSION'];
  }),
  presidentcompensationapproved: computed('model.status', function() {
    let status = this.get('model.status');

    return status === STATUS_MAP['PETITION_FINAL_APPOVAL'];
  }),
};

export {abilityStates};
