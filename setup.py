import distutils.log
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.install import install as _install
import os
import subprocess

with open("version.txt") as f:
    PACKAGE_NAME, VERSION, COMPATIBLE_VERSION = \
        (x.strip() for x in f.read().strip().split())

with open('travelsBackend/requirements.txt') as f:
    INSTALL_REQUIRES = [
        x.strip('\n')
        for x in f.readlines()
        if x and x[0] != '#'
    ]

SHORT_DESCRIPTION = "Travel Expenses"

PACKAGES_ROOT = 'travelsBackend'
PACKAGES = find_packages(PACKAGES_ROOT)

# Package meta
CLASSIFIERS = []

EXTRAS_REQUIRES = {
}

TESTS_REQUIRES = [
]


def get_all_data_files(dest_path, source_path):
    dest_path = dest_path.strip('/')
    source_path = source_path.strip('/')
    source_len = len(source_path)
    return [
        (
            os.path.join(dest_path, path[source_len:].strip('/')),
            [os.path.join(path, f) for f in files],
        )
        for path, _, files in os.walk(source_path)
    ]


UI_DATA_FILES = get_all_data_files('lib/travel/www/ui', 'travelsFront/dist')

TRAVEL_TEMPLATE_FILES = get_all_data_files('lib/travel/resources/templates',
                                           'travelsBackend/texpenses/templates')
TRAVEL_VISUALIZATIONS_FILES = get_all_data_files('lib/travel/visualizations', 'travelsBackend/visualizations')

class BuildUiCommand(_build_py):
    """ Extend build_py to build Travel UI. """

    description = 'build Travel UI'
    user_options = _build_py.user_options + [
        ('no-ui', None, 'skip Travel UI build'),
    ]

    boolean_options = _build_py.boolean_options + ['no-ui']

    def initialize_options(self):
        """ Set default values for options. """

        _build_py.initialize_options(self)
        self.no_ui = None

    def run(self):

        if not self.no_ui:
            command = ['./build_ui.sh', 'production']
            self.announce('building ui: %s' % ' '.join(command),
                          level=distutils.log.INFO)
            subprocess.call(command, cwd='./travelsFront/')

        _build_py.run(self)


class InstallCommand(_install):
    """ Extend install command with --no-build-ui option. """

    user_options = _install.user_options + [
        ('no-build-ui', None, 'skip Travel UI build'),
    ]

    boolean_options = _install.boolean_options + ['no-build-ui']

    def initialize_options(self):
        """ Set default values for options. """

        _install.initialize_options(self)
        self.no_build_ui = None

    def run(self):
        if self.no_build_ui:
            self.reinitialize_command('build_py', no_ui=True)

        _install.run(self)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license='GPLv3',
    description=SHORT_DESCRIPTION,
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    package_dir={'': PACKAGES_ROOT},
    data_files=[
        ('lib/travel/resources',
         [
             'resources/common.json',
             'resources/unaccent_greek.rules',
             'travelsBackend/texpenses/data/countries-full.csv',
             'travelsBackend/texpenses/data/countriesTZ.csv',
             'travelsBackend/texpenses/data/ListEfories.csv',
             'travelsBackend/texpenses/data/ListProjects.csv',
             'travelsBackend/texpenses/fixtures/data.json',
         ]),
        ('lib/travel/scripts', ['scripts/travel_init.sh']),
    ] + UI_DATA_FILES + TRAVEL_TEMPLATE_FILES + TRAVEL_VISUALIZATIONS_FILES,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    tests_require=TESTS_REQUIRES,

    entry_points={
        'console_scripts': [
            'travel = texpenses.management:main',
        ],
    },
    cmdclass={'install': InstallCommand, 'build_py': BuildUiCommand},
)
