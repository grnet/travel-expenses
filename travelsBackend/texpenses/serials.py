from django.conf import settings
from django.db.models import Model, BigIntegerField, CharField
from django.db import connections, transaction

connection = connections['default']
ALLOCATION_INCREMENT = getattr(settings, 'SERIAL_ALLOCATION_INCREMENT', 1000)
serials = {}

def get_serial(serial_name, nr=1):
    if nr <= 0:
        raise ValueError("Cannot get %s <= 0 serials" % nr)

    new_serial, max_serial = serials.get(serial_name, (None, None))
    if new_serial is None or new_serial + nr >= max_serial:
        increment = max(nr, ALLOCATION_INCREMENT)
        new_serial, max_serial = allocate_serial(serial_name, increment)

    serials[serial_name] = (new_serial + nr, max_serial)
    return new_serial


class Serials(Model):
    id = CharField(max_length=255, primary_key=True)
    value = BigIntegerField(default=0)

if connection.vendor == 'postgresql':
    import re
    pattern = "^[a-zA-Z0-9_]+$"
    matcher = re.compile(pattern)

    def validate_serial_name(serial_name):
        return matcher.match(serial_name) is not None

    def get_sequence_increment(cursor, serial_name):
        q = "select to_regclass('%s')" % serial_name
        cursor.execute(q)
        r = cursor.fetchone()[0]
        if r is None:
            q = "create sequence %s cache 1 increment %d"
            q %= (serial_name, ALLOCATION_INCREMENT)
            cursor.execute(q)
        q = "select increment_by from %s" % serial_name
        cursor.execute(q)
        return cursor.fetchone()[0]

    def allocate_serial_postgresql(serial_name, increment):
        if serial_name not in serials:
            if not validate_serial_name(serial_name):
                m = "%r is not an acceptable serial name according to %r"
                m %= (serial_name, pattern)
                raise ValueError(m)

        cursor = connection.cursor()
        sequence_increment = get_sequence_increment(cursor, serial_name)
        if increment > sequence_increment:
            m = ("%r: requested increment %d "
                 "is greater than sequence increment %d.")
            m %= (serial_name, increment, sequence_increment)
            raise ValueError(m)

        q = "select nextval('%s')" % serial_name
        cursor.execute(q)
        new_serial = cursor.fetchone()[0]
        return new_serial, new_serial + sequence_increment

    allocate_serial = allocate_serial_postgresql

else:

    def allocate_serial_generic(serial_name, increment):
        # If serials are output in I/O that will not rollback when a
        # transaction is aborted this must be run outside atomic blocks. If
        # ATOMIC_REQUESTS is enabled, you must run it in a middleware.
        # Middleware run before ATOMIC_REQUESTS takes effect.

        if increment <= 0:
            raise ValueError("Cannot allocate %s <= 0 serials" % increment)

        # # Not bailing out if in atomic block. Let the caller decide if they
        # # can live with rolling back allocations or not.
        # connection.validate_no_atomic_block()

        with transaction.atomic():
            serialob, created = Serials.objects.select_for_update().\
                                get_or_create(id=serial_name)
            new_serial = serialob.value
            max_serial = new_serial + increment
            serialob.value = max_serial
            serialob.save()

        return new_serial, max_serial

    allocate_serial = allocate_serial_generic
