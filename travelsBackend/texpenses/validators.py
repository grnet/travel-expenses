from django.core.exceptions import ValidationError


def iban_validation(iban):
    """TODO: Docstring for is_valid.

    :iban: a string representation of iban
    :returns: boolean

    """
    ibanString = str(iban)
    ibanString = ibanString.strip()
    if ibanString is None or ibanString == "":
        raise ValidationError("IBAN is empty.Please import a 27 letters IBAN")

    if " " in ibanString:
        raise ValidationError("IBAN sould not contain spaces")

    ibanLength = len(ibanString)

    if ibanLength != 27:
        raise ValidationError("IBAN should be a 27 letters alphanumeric")

    ibanString = ibanString.upper()
    countryCode = ibanString[0:2]

    if countryCode != "GR":
        raise ValidationError("IBAN country code:" + countryCode + " is not GR")

    iban_check_digits = ibanString[2:4]

    print "iban_check_digits:" + iban_check_digits

    bban = ibanString[4:]
    print "BBAN:" + bban

    bank_code = bban[0:3]
    print "Bank code:" + bank_code

    bank_store = bban[3:7]
    print "Bank store code:" + bank_store

    customer_code = bban[7:]
    print "Customer code:" + customer_code

    return True
