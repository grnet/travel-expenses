from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


def iban_validation(iban):

    ibanString = str(iban)
    ibanString = ibanString.strip()

    if ibanString is None or ibanString == "":
        msg = "IBAN is empty.Please import a 27 letters IBAN"
        logger.error(msg)
        raise ValidationError(msg)

    if " " in ibanString:
        msg = "IBAN sould not contain spaces"
        logger.error(msg)
        raise ValidationError(msg)

    ibanLength = len(ibanString)

    if ibanLength != 27:
        msg = "IBAN should be a 27 letters alphanumeric"
        logger.error(msg)
        raise ValidationError(msg)

    ibanString = ibanString.upper()
    countryCode = ibanString[0:2]

    if countryCode != "GR":
        msg = "IBAN country code:" + countryCode + " is not GR"
        logger.error(msg)
        raise ValidationError(msg)
    try:
        iban_check_digits = ibanString[2:4]
        int(iban_check_digits)
        print "iban_check_digits:" + iban_check_digits

        bban = ibanString[4:]
        int(bban)
        print "BBAN:" + bban

        bank_code = bban[0:3]
        int(bank_code)
        print "Bank code:" + bank_code

        bank_store = bban[3:7]
        int(bank_store)
        print "Bank store code:" + bank_store

        customer_code = bban[7:]
        int(customer_code)
        print "Customer code:" + customer_code
    except ValueError:
        msg = "IBAN should contain only numbers apart"\
            " from the first 2 letters (GR)"
        logger.error(msg)
        raise ValidationError(msg)


def afm_validator(afm):

    # afmString = str(afm)
    # afmString = afmString.strip()

    # if afmString is None or afmString == "":
    # raise ValidationError("AFM is empty. Please import a 9 digits AFM")
    # afmStringLength = len(afmString)
    # if afmStringLength != 9:
    # raise ValidationError("AFM should be a 9 digits number")

    if afm is None:
        msg = "AFM is empty."
        logger.error(msg)
        raise ValidationError(msg)
    if afm == 0:
        msg = "AFM should not be zero"
        logger.error(msg)
        raise ValidationError(msg)

    afmString = str(afm)
    afmString = afmString.strip()
    afmString_length = len(afmString)
    if len(afmString) != 9:
        msg = "AFM should be a 9 digits number,\
            current length:" + str(afmString_length)
        logger.error(msg)
        raise ValidationError(msg)
