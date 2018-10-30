# !/usr/bin/python
# coding: utf8
import os


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config(object):
    # Running options
    HOST = 'localhost'
    PORT = 7777
    DEBUG = False
    TESTING = False

    # Complex random value use to sign cookies and other things by Flask
    SECRET_KEY = "xxx"
    WTF_CSRF_SECRET_KEY = 'zzz'

    # SQL Alchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(BASE_DIR, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = False

    # CELERY
    # please harden your RabbitMQ installation by removing the default "admin" and "guest" user credentials
    CELERY_BROKER_URL = 'amqp://guest:guest@0.0.0.0:5672//'
    CELERY_RESULT_BACKEND = 'db+sqlite:///celery.sqlite'
    CELERY_TRACK_STARTED = True
    CELERY_IGNORE_RESULT = False

    # max file size allowed (for file upload)
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024

    """
    FILES/FOLDERS LOCATIONS
    """
    # app location
    APP_LOCATIONS = {
        # hashcat executable location
        "hashcat": BASE_DIR + '/hashcat/hashcat64.bin',
    }

    # in case of concat with BASE_DIR, folder values must start and end with separator "/"
    locations_base_dir = os.path.join(BASE_DIR, 'io')
    DIR_LOCATIONS = {

        # Wordlist directory path, by default '/usr/share/wordlists/' on Kali
        'wordlists': locations_base_dir + '/sources/words',

        # Folder directory path, where rules are stored
        'rules': locations_base_dir + '/sources/rules',

        # Output hashcat directory path
        'hashcat_outputs': locations_base_dir + '/outputs',

        # tmp folder
        'tmp': locations_base_dir + '/tmp/'

        # Output logfiles directory path
        # 'log': BASE_DIR + '/outputs/logs/',
        # Upload user files directory
        # 'upload': BASE_DIR + '/outputs/uploads/',
        # John executable path (only used to extract the hash from uploaded encrypted files)
        # by default '/usr/sbin/john' on Kali
        # 'john': BASE_DIR + '/john/',
    }

    # by default wordlists are displayed by filename in "add crack" form.
    # This config allow to define custom wordlists names
    # dict keys are rule path relative to above DIR_LOCATIONS["wordlists"]
    # wordlist files will be displayed on form in order of the following list (wordlist files not defined in the
    # list below will be displayed alphabetically after.
    WORDLIST_SETUP = [
        # EXAMPLE
        # {
        #     # file relative path from DIR_LOCATIONS["wordlists"]
        #     "file": "word3.txt",
        #     # name displayed in form
        #     "name": "Word File n°3",
        #     # is the file selected by default for each attack (optional, default is False)
        #     "active": False
        # },
    ]

    # by default rules are displayed by filename in "add crack" form.
    # This config allow to define custom rules names
    # dict "file" key are rule path relative to above DIR_LOCATIONS["rules"]
    # rules files will be displayed on form in order of the following list (rules files not defined in the
    # list below will be displayed alphabetically after.
    RULES_SETUP = [
        # EXAMPLE
        # {
        #     # file relative path from DIR_LOCATIONS["rules"]
        #     "file": "rule0_last.txt",
        #     # name displayed in form
        #     "name": "My Rule 3",
        #     # is the file selected by default for each rule attack (optional, default is False)
        #     "active": False
        # },
    ]

    """
    ADDITIONAL SETTINGS
    Default values work, but can be adjusted to your needs
    """

    # Authentication settings, choose between "None", "Basic" and "LDAP"
    AUTH_TYPE = "None"

    # Detault users created by the flask deploy command (passwords are encrypted on user creation, see User model)
    DEFAULT_USERS = [
            {
                "name": "admin",
                "email": "admin@admin.com",
                "password": "toto",
                "admin": True
            },
            {
                "name": "admin2",
                "email": "admin2@admin.com",
                "password": "toto",
                "admin": True
            },
            {
                "name": "user",
                "email": "user@user.com",
                "password": "toto",
                "admin": False
            },
            {
                "name": "user2",
                "email": "user2@user.com",
                "password": "toto",
                "admin": False
            }
        ]

    # LDAP settings
    LDAP_HOST = "1.1.1.1"
    LDAP_TLS = True
    LDAP_PORT = 636
    LDAP_NAME = "My LDAP"
    LDAP_BASE_DN = "OU=xxx, OU=xxx, DC=xxx, DC=xxx"
    LDAP_SEARCH_FILTER = "(&(sAMAccountName=%s)(memberOf=CN=xxx,OU=xxx,OU=xxx,DC=xxx,DC=xxx))"

    # Separator char for hashlists/outfile
    HASHLIST_FILE_SEPARATOR = '~'

    # Maximal parallel cracking sessions
    MAX_CRACKSESSIONS = 8

    # Sleeping time when an Out Of Memory exception occured
    OOM_DELAY_SLEEP = 15 * 60

    # John dictionary/Useful to extract hash from files protected by password
    extensions_dictionary = {
        '7z': '7z2john.py',
        'pdf': 'pdf2john.py', 'doc': 'office2john.py',
        'docm': 'office2john.py',
        'dotx': 'office2john.py',
        'dotm': 'office2john.py',
        'xls': 'office2john.py',
        'xlsx': 'office2john.py',
        'ppt': 'office2john.py',
        'pptx': 'office2john.py',
        'docx': 'office2john.py',
        'odf': 'odf2john.py',
        'zip': 'zip2john'
    }
    ALLOWED_EXTENSIONS = set(extensions_dictionary.keys())

    # Crack durations timeout, in days
    CRACK_DURATIONS = [3, 7, 30]

    # Disable hashcat pot file, add "--potfile-disable" to hashcat command
    HASHCAT_DISABLE_POT_FILE = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(BASE_DIR, 'app', 'tests', 'data.sqlite')


class ProductionConfig(Config):
    # no default users created on prod environnement
    DEFAULT_USERS = []


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

