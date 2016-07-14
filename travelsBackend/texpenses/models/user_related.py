from django.db import models
from djago.conf import settings
from django.contrib.auth.models import AbstractUser
from texpenses.validators import afm_validator, iban_validation
from texpenses.models import common


