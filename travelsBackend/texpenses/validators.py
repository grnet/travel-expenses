from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import logging

logger = logging.getLogger(__name__)


iban_validation = RegexValidator(
    r'^^GR\d{9}[0-9A-Z]{16}$', 'IBAN number is not valid.')


def required_validator(obj, required_fields):
    for field in required_fields:
        if not getattr(obj, field, None):
            raise ValidationError('Field %s is required' % repr(field))


def afm_validator(afm):

    if afm is None:
        msg = "AFM is empty."
        logger.error(msg)
        raise ValidationError(msg)
    if afm == 0:
        msg = "AFM should not be zero"
        logger.error(msg)
        raise ValidationError(msg)

    # afmString = str(afm)
    afmString = afm.strip()
    print afmString
    afmString_length = len(afmString)
    if len(afmString) != 9:
        msg = "AFM should be a 9 digits number,current length:" + \
            str(afmString_length)
        logger.error(msg)
        raise ValidationError(msg)
    for digit in afmString:
        try:
            int(digit)
        except ValueError:
            msg = "AFM should contain only digits."
            raise ValidationError(msg)

    afm = map(int, list(str(afmString)))

    if sum(afm) == 0:
        msg = "AFM should not be zero."
        raise ValidationError(msg)

    afm_sum = 0
    afm_length_for_calculations = afmString_length - 1
    for afm_digit in range(0, afm_length_for_calculations, 1):
        power = afm_length_for_calculations - afm_digit
        product = afm[afm_digit] * pow(2, power)
        afm_sum += product

    remainder = afm_sum % 11
    afm_last_digit = afm[afm_length_for_calculations]

    if remainder != afm_last_digit:
        msg = "Specific AFM value does not conform to AFM general rules."
        raise ValidationError(msg)


def date_validator(start_date, end_date, labels):
    """
    This validator checks if two given dates (starting date and ending date)
    are valid.

    Valid dates are dates which are after today and starting date is before
    ending date.

    :param start_date: Starting date.
    :param end_date: Ending date.
    :labels: tuple which contains labels for the start_date and end_date
    fields respectively.

    :raises: VallidationError if two given dates are not valid.
    """
    now = datetime.now()
    start_label, end_label = labels
    if start_date < now:
        raise ValidationError('%s date should be after today' % (start_label))

    if end_date < now:
        raise ValidationError('%s should be after today' % (end_label))

    if end_date < start_date:
        raise ValidationError(
            '%s date should be after %s date' % (
                end_label, start_label))
