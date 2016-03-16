from django.core.exceptions import ValidationError


def is_valid(iban):
    """TODO: Docstring for is_valid.

    :iban: a string representation of iban
    :returns: boolean

    """
    ibanString = str(iban)
    ibanString = ibanString.strip()
    if ibanString is None or ibanString == "":
        return False
    if " " in ibanString:
        return False
    if len(ibanString) < 2:
        return False

    ibanString = ibanString.upper()
    countryCode = ibanString[0:2]

    if countryCode != "GR":
        print countryCode
        return False

    return True


def validate_iban(iban):
    """TODO: Docstring for .

    :validate_iban(iban: TODO
    :returns: TODO

    """
    if(not is_valid(iban)):
        raise ValidationError("Iban value:" + iban + " is not valid")
