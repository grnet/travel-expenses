PERMISSION_RULES = [
    ('resources/tax-office', 'list', 'anonymous', '*', '*', '*'),
    ('resources/tax-office', 'retrieve', 'anonymous', '*', '*', '*'),

    ('resources/project', 'list', 'anonymous', '*', '*', '*'),
    ('resources/project', 'retrieve', 'anonymous', '*', '*', '*'),

    ('resources/countries', 'list', 'anonymous', '*', '*', '*'),
    ('resources/countries', 'retrieve', 'anonymous', '*', '*', '*'),

    ('resources/city', 'list', 'anonymous', '*', '*', '*'),
    ('resources/city', 'retrieve', 'anonymous', '*', '*', '*'),

    ('users', 'retrieve', 'USER', '*', '*', '*'),
    ('users', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('users', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('users', 'retrieve', 'CONTROLLER', '*', '*', '*'),

    ('petition/user/saved', 'create', 'USER', '*', '*', '*'),
    ('petition/user/saved', 'list', 'USER', '*', '*', '*'),
    ('petition/user/saved', 'retrieve', 'USER', '*', '*', '*'),
    ('petition/user/saved', 'update', 'USER', '*', '*', '*'),
    ('petition/user/saved', 'destroy', 'USER', '*', '*', '*'),

    ('petition/user/submitted', 'create', 'USER', '*', '*', '*'),
    ('petition/user/submitted', 'cancel', 'USER', '*', '*', '*'),
    ('petition/user/submitted', 'list', 'USER', '*', '*', '*'),
    ('petition/user/submitted', 'retrieve', 'USER', '*', '*', '*'),
    ('petition/user/submitted', 'update', 'USER', '*', '*', '*'),

    ('petition/secretary/saved', 'create', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/saved', 'list', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/saved', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/saved', 'list', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/saved', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/saved', 'update', 'SECRETARY', '*', '*', '*'),

    ('petition/secretary/submitted', 'create', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/submitted', 'list', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/submitted', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/submitted', 'list', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/submitted', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/submitted', 'update', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/submitted', 'cancel', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/submitted',
     'president_approval', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/submitted',
     'application_report', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/submitted',
     'decision_report', 'SECRETARY', '*', '*', '*'),

    ('petition/user/compensations', 'create', 'USER', '*', '*', '*'),
    ('petition/user/compensations', 'update', 'USER', '*', '*', '*'),
    ('petition/user/compensations', 'list', 'USER', '*', '*', '*'),
    ('petition/user/compensations', 'retrieve', 'USER', '*', '*', '*'),
    ('petition/user/compensations', 'save', 'USER', '*', '*', '*'),
    ('petition/user/compensations', 'submit', 'USER', '*', '*', '*'),
    ('petition/user/compensations', 'cancel', 'USER', '*', '*', '*'),


    ('petition/secretary/compensations', 'create', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations', 'list', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations',
     'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations', 'update', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations', 'cancel', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations',
     'president_approval', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations',
     'application_report', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations',
     'decision_report', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations', 'save', 'CONTROLLER', '*', '*', '*'),
    ('petition/secretary/compensations', 'submit', 'CONTROLLER', '*', '*', '*'),


    ('petition/secretary/compensations', 'list', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/compensations',
     'retrieve', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/compensations', 'update', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/compensations', 'cancel', 'SECRETARY', '*', '*', '*'),


]
