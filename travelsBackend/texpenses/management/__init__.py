import os
import sys
from django.core.management import ManagementUtility


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelsBackend.settings")
    mu = ManagementUtility(sys.argv)
    mu.execute()

if __name__ == "__main__":
    main()
