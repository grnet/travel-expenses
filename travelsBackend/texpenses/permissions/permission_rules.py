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
    ('petition/user/saved', 'delete', 'USER', '*', '*', '*'),

    ('petition/user/submitted', 'create', 'USER', '*', '*', '*'),
    ('petition/user/submitted', 'list', 'USER', '*', '*', '*'),
    ('petition/user/submitted', 'retrieve', 'USER', '*', '*', '*'),
    ('petition/user/submitted', 'update', 'USER', '*', '*', '*'),
    ('petition/user/submitted', 'delete', 'USER', '*', '*', '*'),

    ('petition/secretary/saved', 'create', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/saved', 'list', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/saved', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/saved', 'update', 'SECRETARY', '*', '*', '*'),
    ('petition/secretary/saved', 'delete', 'SECRETARY', '*', '*', '*')
]
