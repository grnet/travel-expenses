from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import logging

logger = logging.getLogger(__name__)


iban_validation = RegexValidator(
    r'^GR(?:\s*[0-9a-zA-Z]\s*){20}$', 'IBAN number is not valid.')


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
