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

        bban = ibanString[4:]
        int(bban)

        bank_code = bban[0:3]
        int(bank_code)

        bank_store = bban[3:7]
        int(bank_store)

        customer_code = bban[7:]
        int(customer_code)
    except ValueError:
        msg = "IBAN should contain only numbers apart"\
            " from the first 2 letters (GR)"
        logger.error(msg)
        raise ValidationError(msg)


def afm_validator(afm):

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
    # nSum = 0
    # xDigit = 0
    # nT = 0
    # nExp = 1

    # for i in range(afmString_length - 2, 0, -1):
        # afmSubString = afmString[i:0:-1]
        # xDigit = int(afmSubString)
        # nT = xDigit * int(pow(2, nExp))
        # nSum += nT
        # nExp += 1
    # xDigit = int(afmString[afmString_length - 1:1:-1])
    # nT = nSum / 11
    # k = nT * 11
    # k = nSum - k
    # print "K:" + str(k)
    # print "xDigit:" + str(xDigit)

    # if k == 10:
        # k = 0
    # if xDigit != k:
        # msg = "AFM does not conform to specific AFM rules."
        # return ValidationError(msg)
