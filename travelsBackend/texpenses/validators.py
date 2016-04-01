from django.core.exceptions import ValidationError


def iban_validation(iban):

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
        raise ValidationError(
            "IBAN should contain only numbers apart"
            " from the first 2 letters (GR)")


def afm_validator(afm):

    # afmString = str(afm)
    # afmString = afmString.strip()

    # if afmString is None or afmString == "":
    # raise ValidationError("AFM is empty. Please import a 9 digits AFM")
    # afmStringLength = len(afmString)
    # if afmStringLength != 9:
    # raise ValidationError("AFM should be a 9 digits number")

    if afm is None:
        raise ValidationError("AFM is empty.")
    if afm == 0:
        raise ValidationError("AFM should not be zero")

    afmString = str(afm)
    afmString = afmString.strip()
    afmString_length = len(afmString)
    if len(afmString) != 9:
        raise ValidationError(
            "AFM should be a 9 digits number,"\
            " current length:" + str(afmString_length))
